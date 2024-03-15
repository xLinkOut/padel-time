#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask_login import login_required


view_bp = Blueprint("view", __name__)

@view_bp.get("/login")
def login():
    return render_template("auth/login.html")

@view_bp.get("/signup")
def signup():
    return render_template("auth/signup.html")

@view_bp.get("/")
@view_bp.get("/dashboard")
@login_required
def dashboard():  
    return render_template("dashboard/dashboard.html")