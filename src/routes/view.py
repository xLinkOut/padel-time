#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user


view_bp = Blueprint("view", __name__)

@view_bp.get("/login")
def login():
    return render_template("auth/login.html")

@view_bp.get("/signup")
def signup():
    return render_template("auth/signup.html")

@view_bp.get("/")
@view_bp.get("/dashboard")
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for("view.login"))
    
    return render_template("dashboard/dashboard.html")