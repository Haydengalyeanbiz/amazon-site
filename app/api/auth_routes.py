from flask import Blueprint, request
from app.models import User, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/')
def authenticate():
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'errors': {'message': 'Unauthorized'}}, 401

@auth_routes.route('/login-for-mom', methods=['POST'])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.data['email']).first()
        login_user(user)
        return user.to_dict()
    return form.errors, 401

@auth_routes.route('/logout', methods=["POST"])
def logout():
    logout_user()
    return {'message': 'User logged out'}