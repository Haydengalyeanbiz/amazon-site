from .db import db,environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    
    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    image_url = db.Column(db.String(1200), nullable=False)
    link_url = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'price': self.price,
            'description': self.description,
            'image_url': self.image_url,
            'link_url': self.link_url,
        }