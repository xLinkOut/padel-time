#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from flask_login import current_user, login_user, logout_user
from models import db, User
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)

@auth.post("/signup")
def signup():
    data = request.get_json()

    if not (email := data.get("email")):
        return {"success": False, "message": "Email field is required"}, 400
    
    if not (password := data.get("password")):
        return {"success": False, "message": "Password field is required"}, 400
    
    if User.query.filter_by(email=email).first():
        return {"success": False, "message": "A user with that email already exists"}, 409
    
    user = User(email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return {"success": True, "data": {"id": user.id}}, 201


@auth.post("/login")
def login():
    data = request.get_json()

    if not (email := data.get("email")):
        return {"success": False, "message": "Email field is required"}, 400
    
    if not (password := data.get("password")):
        return {"success": False, "message": "Password field is required"}, 400
    
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return {"success": False, "message": "Invalid credentials"}, 401
    
    login_user(user)
    user.last_login_at = db.func.now()
    db.session.commit()

    return {"success": True, "data": {"id": user.id}}, 200


@auth.post("/logout")
def logout():
    if not current_user.is_authenticated:
        return {"success": False, "message": "Not logged in"}, 400
    
    logout_user()
    return {"success": True}
