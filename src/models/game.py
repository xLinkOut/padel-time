#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.DateTime, nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "slot": self.slot.isoformat(),
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "players": [match_user.user.to_dict() for match_user in self.players],
        }
