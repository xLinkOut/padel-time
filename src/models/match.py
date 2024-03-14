#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models import db


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_date = db.Column(db.DateTime, nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "match_date": self.match_date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "players": [match_user.user.to_dict() for match_user in self.players],
        }
