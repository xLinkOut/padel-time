#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models import db


class GameUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    game = db.relationship("Game", backref="players", lazy=True)
    user = db.relationship("User", backref="game_users")

    __table_args__ = (db.UniqueConstraint("game_id", "user_id"),)

    def to_dict(self):
        return {"id": self.id, "game_id": self.game_id, "user_id": self.user_id}
