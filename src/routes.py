#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
from typing import Any, Optional
from flask import Blueprint, current_app, request
from flask_login import current_user, logout_user
from models import db, User
from werkzeug.security import check_password_hash, generate_password_hash
import jwt

auth = Blueprint("auth", __name__)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not (token := request.headers.get("Authorization", "").replace("Bearer ", "")):
            return {"success": False, "message": "Authorization header is required"}, 401

        try:
            data = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
            if not (user := User.query.get(data.get("id"))):
                return {"success": False, "message": "Invalid authentication token"}, 401
            
            current_user.set(user)
        except Exception as e:
            return {"success": False, "message": "Invalid authentication token"}, 401
        
        return f(user, *args, **kwargs)
    
    return decorated


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
    
    response = {
        "id": user.id,
        "role": user.role
    }

    token = jwt.encode(
        response,
        current_app.secret_key,
        algorithm="HS256"
    )
    
    user.last_login_at = db.func.now()
    db.session.commit()

    return {"success": True, "data": {**response, "token": token}}, 200
