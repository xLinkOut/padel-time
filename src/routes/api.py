#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Blueprint, current_app, request
from flask_login import current_user, login_required

from models import db
from models.game import Game
from models.match_user import MatchUser
from models.reservation import Reservation
from models.user import UserRole

api_bp = Blueprint("api", __name__)


@api_bp.get("/matches")
@login_required
def get_matches():
    filters = []

    if slot := request.args.get("slot"):
        filters.append(Game.slot == slot)
    if current_user.role != UserRole.ADMIN.value:
        filters.append(MatchUser.user_id == current_user.id)
    elif user_id := request.args.get("user_id"):
        filters.append(MatchUser.user_id == user_id)

    matches = Game.query.join(MatchUser).filter(*filters).all()
    return {"success": True, "data": [match.to_dict() for match in matches]}, 200


@api_bp.get("/matches/<int:match_id>")
@login_required
def get_match(match_id):
    filters = [Game.id == match_id]
    if current_user.role != UserRole.ADMIN.value:
        filters.append(MatchUser.user_id == current_user.id)
    
    match = Game.query.join(MatchUser).filter(*filters).first()
    if not match:
        return {"success": False, "message": "Match not found"}, 404

    return {"success": True, "data": match.to_dict()}, 200
