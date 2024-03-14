#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models import db


class GameUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id", ondelete="cascade"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="cascade"), nullable=False, index=True)

    __table_args__ = (db.UniqueConstraint("game_id", "user_id"),)

    def to_dict(self):
        return {"id": self.id, "game_id": self.game_id, "user_id": self.user_id}
