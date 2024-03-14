#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import current_app
from models import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.DateTime, nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    organizer = db.relationship("User", backref="created_games")

    def to_dict(self):
        return {
            "id": self.id,
            "slot": self.slot.isoformat(),
            "created_at": self.created_at.isoformat(),
            "created_by": self.organizer.to_dict(),
            "ready": len(self.players) == current_app.players_for_game,
            "players": [game_user.user.to_dict() for game_user in self.players],
        }
