from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from .models import db, User
from .config import Config
from .seeders import seed_commands
from .api.auth_routes import auth_routes
from .api.post_routes import post_routes

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')

login = LoginManager(app)
login.login_view = 'auth.unauthorized'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

app.cli.add_command(seed_commands)

app.config.from_object(Config)

# ! BLUEPPRINTS GO HERE
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(post_routes, url_prefix='/api/posts')

Migrate(app, db)
CORS(app)