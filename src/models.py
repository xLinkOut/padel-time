#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import enum
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class UserRole(enum.Enum):
    USER = 1
    ADMIN = 2

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(512), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=UserRole.USER.value)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    last_login_at = db.Column(db.DateTime, nullable=True)
    
    # Flask-Login integration
    def get_id(self):
        return str(self.id)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    
    user = db.relationship('User', backref='reservations', lazy=True)
