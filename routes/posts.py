# src/posts.py
# This file holds API routes for post functionality and nav
from . import posts_bp
import os
from flask import jsonify, render_template, redirect, request, session, flash
from src.post_utils import *

TOKEN = os.getenv('API_KEY')

temp = 'temp'

@posts_bp.post('/posts/generate')
def generate_post():
    """
    Data will hold all information about the new post
    title - The title of the new post
    description - the description/prompt for the post
    image - a blob or b64 encoded image
    """
    data = request.get_json()
    print(data)
 
    data['image'] = invert_ctrl_image(data['image'])
    decode_image(data["image"], f'./uploads/input.jpg') 
    
    # TODO: Create a post in the DB, flagged as pending
    if 'user_id' not in session:
        return { "response": 401, "message": "You must be logged in to create a post" }

    generated = queue_image_generation(0, data['description'], data['image'])
    
    user_id = session['user_id']
    post = create_post(generated, data['title'], data['description'], user_id)

    print(f'Generated an image!')
    return { "response": 200, "post_id": post.post_id }


@posts_bp.get('/posts/create')
def new_post():
    if 'user_id' not in session:
        flash('You must be logged in to create a post')
        return redirect('/users/login')
        
    return render_template('new_post.html')


@posts_bp.get('/posts/<post_id>')
def post_detail(post_id):
    if request.accept_mimetypes.best == 'application/json':
        post = get_post_by_id(post_id)
        if post is None:
            return { "response": 404, "message": f"Post with id {post_id} not found" }
        return { "response": 200, "image": post.image.decode() } 
    else:
        post = get_post_by_id(post_id)
        if not post:
            flash('Post not found.')
            return redirect('/')
        comments = get_comments_for_post(post_id)
        user_id = session.get('user_id')
        has_liked = check_user_like(user_id, post_id)
        like_count = get_like_count(post_id)

        return render_template('view_post.html', post=post, comments=comments, has_liked=has_liked, like_count=like_count, post_id=post_id)


@posts_bp.route('/posts')
def posts():
    return render_template('posts.html')


def is_logged_in():
    return 'user_id' in session

# comment routes
@posts_bp.post('/posts/<int:post_id>/comment')
def post_comment(post_id):
    if not is_logged_in():
        flash('You must be logged in to comment.')
        return redirect('/users/login')

    text = request.form['text']
    create_comment(post_id, session['user_id'], text)
    flash('Comment posted successfully.')
    return redirect(f'/posts/{post_id}')


@posts_bp.post('/posts/<int:post_id>/comments/<int:comment_id>/edit')
def edit_comment(post_id, comment_id):
    if not is_logged_in():
        flash('You must be logged in to edit comments.')
        return redirect('/users/login')

    comment = get_comment_by_id(comment_id)
    if comment.author_id != session['user_id']:
        flash('You can only edit your own comments.')
        return redirect(f'/posts/{post_id}')

    text = request.form['text']
    if update_comment(comment_id, text):
        flash('Comment updated successfully.')
    else:
        flash('Error updating comment.')
    return redirect(f'/posts/{post_id}')


@posts_bp.post('/posts/<int:post_id>/comments/<int:comment_id>/delete')
def delete_comment_route(post_id, comment_id):
    if not is_logged_in():
        flash('You must be logged in to delete comments.')
        return redirect('/users/login')

    comment = get_comment_by_id(comment_id)
    if comment.author_id != session['user_id']:
        flash('You can only delete your own comments.')
        return redirect(f'/posts/{post_id}')

    if delete_comment(comment_id):
        flash('Comment deleted successfully.')
    else:
        flash('Error deleting comment.')
    return redirect(f'/posts/{post_id}')


@posts_bp.post('/posts/<int:post_id>/like')
def like_post_route(post_id):
    if not is_logged_in():
        return jsonify({"status": "error", "message": "You must be logged in to like a post."}), 401

    action = like_post(session['user_id'], post_id)
    new_like_count = get_like_count(post_id)  
    return jsonify({"status": "success", "action": action, "new_like_count": new_like_count}), 200

