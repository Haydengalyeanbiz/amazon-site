from flask import Blueprint, request, jsonify
from app.models import Post, db
from app.forms import PostForm
from flask_login import login_required, current_user
from datetime import datetime

post_routes = Blueprint('post', __name__)

#*--------------------------Get All Posts------------------------
@post_routes.route('/all-posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.created_date.desc()).all()
    result = [post.to_dict() for post in posts]
    return jsonify(result), 200

#*--------------------------Get A Single Post------------------------
@post_routes.route('/api/posts/<int:post_id>', methods=['GET'])
def get_single_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    post_data = {
        'id': post.id,
        'title': post.title,
        'price': post.price,
        'description': post.description,
        'image_url': post.image_url,
        'link_url': post.link_url,
        'author_id': post.user_id,  # Include author information if needed
    }
    return jsonify(post_data), 200

#*------------------------Submit a Post----------------------------
@post_routes.route('/submit-post', methods=['POST'])
@login_required
def submit_post():
    form = PostForm(data=request.json)
    form['csrf_token'].data = request.cookies.get('csrf_token')

    if not form.validate():
        print("Form validation errors:", form.errors)
        errors = {field: error[0] for field, error in form.errors.items()}
        return jsonify({'error': 'Form validation failed', 'details': errors}), 400

    new_post = Post(
        title=form.title.data,
        price=form.price.data,
        description=form.description.data,
        image_url=form.image_url.data,
        link_url=form.link_url.data,
        user_id=current_user.id, 
        created_date=datetime.utcnow(),
    )

    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'}), 201

#*------------------------Update a Post----------------------------
@post_routes.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.json  

    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # Update the post fields with the new data
    if 'title' in data:
        post.title = data['title']
    if 'price' in data:
        post.price = data['price']
    if 'description' in data:
        post.description = data['description']
    if 'image_url' in data:
        post.image_url = data['image_url']
    if 'link_url' in data:
        post.link_url = data['link_url']

    try:
        db.session.commit()
        return jsonify({
            'message': 'Post updated successfully',
            'post': {
                'id': post.id,
                'title': post.title,
                'price': post.price,
                'description': post.description,
                'image_url': post.image_url,
                'link_url': post.link_url
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update post', 'details': str(e)}), 500
    
#*------------------------Delete a Post----------------------------
@post_routes.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    if post.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized to delete this post'}), 403

    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete post', 'details': str(e)}), 500