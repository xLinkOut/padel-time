#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Blueprint, current_app, request
from flask_login import current_user, login_required

from models import db
from models.game import Game
from models.game_user import GameUser
from models.user import UserRole

api_bp = Blueprint("api", __name__)

@api_bp.get("/games/<int:game_id>")
@login_required
def get_game(game_id):
    filters = [Game.id == game_id]
    
    if current_user.role != UserRole.ADMIN.value:
        filters.append(GameUser.user_id == current_user.id)
    
    if not (game := Game.query.join(GameUser).filter(*filters).first()):
        return {"success": False, "message": "Game not found"}, 404

    return {"success": True, "data": game.to_dict()}, 200


@api_bp.get("/games")
@login_required
def search_games():
    filters = []

    if slot := request.args.get("slot"):
        try:
            slot = datetime.strptime(slot, "%Y-%m-%dT%H:%M:%S").replace(minute=0, second=0)
            filters.append(Game.slot == slot)
        except ValueError:
            return {"success": False, "message": "Invalid date format, must be %Y-%m-%dT%H:%M:%S"}, 400

    if current_user.role != UserRole.ADMIN.value:
        filters.append(GameUser.user_id == current_user.id)
    elif user_id := request.args.get("user_id"):
        filters.append(GameUser.user_id == user_id)

    games = Game.query.join(GameUser).filter(*filters).all()
    return {"success": True, "data": [game.to_dict() for game in games]}, 200


@api_bp.post("/games")
@login_required
def create_game():
    data = request.get_json()

    if not (slots := data.get("slots")):
        return {"success": False, "message": "<slot> field is required"}, 400

    games = []
    current_slot_date = datetime.now().replace(minute=59, second=59)
    
    for slot in slots:
        try:
            slot = datetime.strptime(slot, "%Y-%m-%dT%H:%M:%S").replace(minute=0, second=0)
        except ValueError:
            return {"success": False, "message": "Invalid date format, must be %Y-%m-%dT%H:%M:%S"}, 400

        if not (9 <= slot.hour <= 23):
            return {"success": False, "message": "Games can only be made between 9 and 23"}, 400

        if slot < current_slot_date:
            return {"success": False, "message": "Cannot create a game in the past"}, 400

        game = Game.query.join(GameUser).filter(Game.slot == slot).first()
        
        if game:
            if current_user.id in map(lambda game_user: game_user.user_id, game.players):
                # Potrebbe non essere bloccante, e continuare ad inserire gli eventuali slot successivi
                return {"success": False, "message": "You already have a reservation for that slot"}, 409

            if len(game.players) >= current_app.players_for_game:
                return {"success": False, "message": "There is already a full game scheduled for that slot"}, 409
        else:
            game = Game(slot=slot, created_by=current_user.id)
            db.session.add(game)
        
        games.append(game)

        game_user = GameUser(game=game, user=current_user)
        db.session.add(game_user)

    db.session.commit()

    for game in games:
        # Ci sono abbastanza giocatori per iniziare una partita
        if len(game.players) == current_app.players_for_game:
            # Logica per l'invio di email/notifica, maniera asincrona
            # (Celery+Redis, ad esempio, oppure scheduler in background)
            pass

    return {"success": True, "data": [game.to_dict() for game in games]}, 201

