#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import enum

from flask_login import UserMixin, current_user

from models import db


class UserRole(enum.Enum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(512), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=UserRole.USER.value)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    last_login_at = db.Column(db.DateTime, nullable=True)

    # Flask-Login integration
    def get_id(self):
        return str(self.id)

    def to_dict(self):
        if current_user.role == UserRole.USER.value and current_user.id != self.id:
            return {"id": self.id, "email": self.email}

        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }
