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


@api_bp.get("/games")
@login_required
def get_games():
    filters = []

    if slot := request.args.get("slot"):
        filters.append(Game.slot == slot)
    if current_user.role != UserRole.ADMIN.value:
        filters.append(GameUser.user_id == current_user.id)
    elif user_id := request.args.get("user_id"):
        filters.append(GameUser.user_id == user_id)

    games = Game.query.join(GameUser).filter(*filters).all()
    return {"success": True, "data": [game.to_dict() for game in games]}, 200


@api_bp.get("/games/<int:game_id>")
@login_required
def get_game(game_id):
    filters = [Game.id == game_id]
    if current_user.role != UserRole.ADMIN.value:
        filters.append(GameUser.user_id == current_user.id)
    
    game = Game.query.join(GameUser).filter(*filters).first()
    if not game:
        return {"success": False, "message": "Game not found"}, 404

    return {"success": True, "data": game.to_dict()}, 200
