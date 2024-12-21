from flask.cli import AppGroup
from .users import seed_users, undo_users
from app.models import db, environment, SCHEMA

seed_commands = AppGroup('seed')

@seed_commands.command('all')
def seed():
    print("Running seed command...")
    if environment == 'production':
        print("Environment is production - undoing users first.")
        undo_users()
    seed_users()
    print("Seeding complete.")

@seed_commands.command('undo')
def undo():
    print("Running undo command...")
    undo_users()
    print("Undo complete.")