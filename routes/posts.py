# src/posts.py
# This file holds API routes for post functionality and nav
from . import posts_bp
import os
from flask import render_template, request
from src.post_utils import queue_image_generation, encode_ctrl_image, decode_image

TOKEN = os.getenv('API_KEY')



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
    
    # TODO: Create a post in the DB, flagged as pending

    # TODO: Start an async call to the gen API
    generated = queue_image_generation(0, data['description'], data['image'])

    print(f'Generated an image!')
    
    return { "response": 200, "image": generated }


@posts_bp.get('/new_post')
def new_post():
    return render_template('new_post.html')


@posts_bp.get('/post/<post_id>')
def post_detail(post_id):
    return render_template('post_detail.html', post_id=post_id)
