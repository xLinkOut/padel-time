#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Blueprint, current_app, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from models import Reservation, User, db, Match, MatchUser, UserRole

auth = Blueprint("auth", __name__)
api = Blueprint("api", __name__)


@auth.post("/signup")
def signup():
    data = request.get_json()

    if not (email := data.get("email")):
        return {"success": False, "message": "Email field is required"}, 400

    if not (password := data.get("password")):
        return {"success": False, "message": "Password field is required"}, 400

    if User.query.filter_by(email=email).first():
        return {"success": False, "message": "A user with that email already exists"}, 409

    user = User(email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return {"success": True, "data": {"id": user.id}}, 201


@auth.post("/login")
def login():
    data = request.get_json()

    if not (email := data.get("email")):
        return {"success": False, "message": "Email field is required"}, 400

    if not (password := data.get("password")):
        return {"success": False, "message": "Password field is required"}, 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return {"success": False, "message": "Invalid credentials"}, 401

    login_user(user)
    user.last_login_at = db.func.now()
    db.session.commit()

    return {"success": True, "data": {"id": user.id}}, 200


@auth.post("/logout")
def logout():
    if not current_user.is_authenticated:
        return {"success": False, "message": "Not logged in"}, 400

    logout_user()
    return {"success": True}


@api.post("/reservations")
@login_required
def create_reservations():
    data = request.get_json()

    if not (dates := data.get("dates")):
        return {"success": False, "message": "Dates field is required"}, 400

    current_slot_date = datetime.now().replace(minute=59, second=59)

    for date in dates:
        try:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").replace(minute=0, second=0)
        except ValueError:
            return {"success": False, "message": "Invalid date format, must be %Y-%m-%dT%H:%M:%S"}, 400

        if not (9 <= date.hour <= 23):
            return {"success": False, "message": "Reservations can only be made between 9 and 23"}, 400

        if date < current_slot_date:
            return {"success": False, "message": "Cannot make reservations in the past"}, 400

        if Match.query.filter_by(match_date=date).first():
            return {"success": False, "message": "There is already a match scheduled for that date"}, 409

        # In ogni caso, sul database c'e' un vincolo unique sulla coppia (utente, data)
        # Potrebbe non essere bloccante, andrebbe ad inserire tutte le altre date
        if Reservation.query.filter_by(user_id=current_user.id, match_date=date).first():
            return {"success": False, "message": "You already have a reservation for that date"}, 409

        reservation = Reservation(user=current_user, match_date=date)
        db.session.add(reservation)

    db.session.commit()

    reservation_players = Reservation.query.filter_by(match_date=date).all()
    reservation_players_count = len(reservation_players)

    if reservation_players_count < current_app.players_for_match:
        return {"success": True, "data": {**reservation.to_dict(), "players": len(reservation_players)}}

    elif reservation_players_count == current_app.players_for_match:
        match = Match(match_date=date)
        db.session.add(match)
        for reservation in reservation_players:
            match_user = MatchUser(match=match, user=reservation.user)
            db.session.add(match_user)
        db.session.commit()

        return {"success": True, "data": {**reservation.to_dict(), "players": len(reservation_players), "match": match.to_dict()}}, 201

    return {"success": False, "message": "Too many players for that date"}, 400


@api.get("/reservations")
@login_required
def get_reservations():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()

    # TODO: Una vista con il numero di giocatori per slot potrebbe essere comoda

    return {
        "success": True,
        "data": [
            {
                "players": Reservation.query.filter_by(match_date=reservation.match_date).count(),
                **reservation.to_dict(),
            }
            for reservation in reservations
        ],
    }, 200


@api.get("/reservations/<int:reservation_id>")
@login_required
def get_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation or reservation.user_id != current_user.id:
        return {"success": False, "message": "Reservation not found"}, 404

    return {"success": True, "data": reservation.to_dict()}, 200


@api.delete("/reservations/<int:reservation_id>")
@login_required
def delete_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation or reservation.user_id != current_user.id:
        return {"success": False, "message": "Reservation not found"}, 404

    # Scelta di design: si mantiene lo storico, senza implementare una soft-delete
    if reservation.match_date < datetime.now():
        return {"success": False, "message": "Cannot delete past reservations"}, 400

    if MatchUser.query.join(Match).filter(Match.match_date == reservation.match_date, MatchUser.user_id == current_user.id).first():
        return {"success": False, "message": "Cannot delete a reservation while in a match"}, 400

    db.session.delete(reservation)
    db.session.commit()

    return {"success": True}, 200

@api.get("/matches")
@login_required
def get_matches():
    filters = []

    if match_date := request.args.get("date"):
        filters.append(Match.match_date == match_date)
    if current_user.role != UserRole.ADMIN.value:
        filters.append(MatchUser.user_id == current_user.id)

    matches = Match.query.join(MatchUser).filter(*filters).all()
    return {"success": True, "data": [match.to_dict() for match in matches]}, 200
