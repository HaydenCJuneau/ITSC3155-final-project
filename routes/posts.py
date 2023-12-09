# src/posts.py
# This file holds API routes for post functionality and nav
from . import posts_bp
import os
from flask import render_template, request
from src.post_utils import queue_image_generation, decode_image, invert_ctrl_image

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

    # TODO: Start an async call to the gen API
    generated = queue_image_generation(0, data['description'], data['image'])

    print(f'Generated an image!')
    global temp
    temp = generated
    return { "response": 200 }


@posts_bp.get('/post/create')
def new_post():
    return render_template('new_post.html')


@posts_bp.get('/post/<post_id>')
def post_detail(post_id):
    global temp

    if request.accept_mimetypes['application/json'] > request.accept_mimetypes['text/html']:
        return { "response": 200, "image": temp } 
    else:
        return render_template('view_post.html', post_id=post_id)
