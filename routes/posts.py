# src/posts.py
# This file holds API routes for post functionality and nav
from . import posts_bp
import os
from flask import render_template, redirect, request, session
from src.post_utils import *

TOKEN = os.getenv('API_KEY')

temp = 'temp'

@posts_bp.post('/post/generate')
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


@posts_bp.get('/post/create')
def new_post():
    return render_template('new_post.html')


@posts_bp.get('/post/<post_id>')
def post_detail(post_id):
    if request.accept_mimetypes.best == 'application/json':
        post = get_post_by_id(post_id)
        if post is None:
            return { "response": 404, "message": f"Post with id {post_id} not found" }
        return { "response": 200, "image": post.image.decode() } 
    else:
        return render_template('view_post.html', post_id=post_id)

@posts_bp.route('/posts')
def posts():
    return render_template('posts.html')