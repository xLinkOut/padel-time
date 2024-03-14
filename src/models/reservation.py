#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models import db


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    match_date = db.Column(db.DateTime, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    user = db.relationship("User", backref="reservations", lazy=True)

    __table_args__ = (db.UniqueConstraint("user_id", "match_date"),)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "match_date": self.match_date.isoformat(),
            "created_at": self.created_at.isoformat(),
        }
