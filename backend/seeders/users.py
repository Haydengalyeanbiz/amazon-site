from backend.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text

def seed_users():
    mom = User(
        username='indycouponmama', email='hbennen@yahoo.com',password='DealsMama5742!'
    )
    db.session.add(mom)

def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))
        
    db.session.commit()