from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text
import os

def seed_users():
    mom = User(
        username=os.getenv("USERNAME"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD") 
    )
    db.session.add(mom)
    db.session.commit()

def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))
        
    db.session.commit()