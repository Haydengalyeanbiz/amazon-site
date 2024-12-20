from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from .models import db, User
from .config import Config
from .seeders import seed_commands

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')

login = LoginManager(app)
login.login_view = 'auth.unauthorized'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

app.cli.add_command(seed_commands)

app.config.from_object(Config)

# ! BLUEPPRINTS GO HERE

Migrate(app, db)
CORS(app)