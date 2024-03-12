#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/signup")
def signup():
    pass
