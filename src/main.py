#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

from models import User, db
from routes.api import api_bp
from routes.auth import auth_bp

load_dotenv()

app = Flask(__name__)

# Flask secrets
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Flask login
login_manager = LoginManager()
login_manager.login_view = ""
login_manager.init_app(app)

# Misc
app.players_for_match = int(os.getenv("PLAYERS_FOR_MATCH", 4))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# SQLAlchemy
URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config["SQLALCHEMY_DATABASE_URI"] = URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Database
db.init_app(app)
with app.app_context():
    db.create_all()

# Blueprints
app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/auth")
