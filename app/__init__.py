from flask import Flask, request, redirect
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_cors import CORS
from flask_login import LoginManager
from .models import db, User
from .config import Config
from .seeders import seed_commands
import os

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from .api.auth_routes import auth_routes
    from .api.post_routes import post_routes
    from .api.amazon_routes import amazon_routes

    app.register_blueprint(auth_routes, url_prefix='/api/auth')
    app.register_blueprint(post_routes, url_prefix='/api/posts')
    app.register_blueprint(amazon_routes, url_prefix='/api/amazon')

    app.cli.add_command(seed_commands)

    return app