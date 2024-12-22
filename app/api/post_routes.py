from flask import Blueprint, request, jsonify
from app.models import Post
from app.forms import PostForm
from flask_login import login_required

post_routes = Blueprint('post', __name__)

@post_routes.route('/all-posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.created_date.desc()).all()
    result = [post.to_dict() for post in posts]
    return jsonify(result), 200