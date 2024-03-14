#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models import db


class MatchUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    match = db.relationship("Match", backref="players", lazy=True)
    user = db.relationship("User", backref="match_users")

    __table_args__ = (db.UniqueConstraint("match_id", "user_id"),)

    def to_dict(self):
        return {"id": self.id, "match_id": self.match_id, "user_id": self.user_id}
