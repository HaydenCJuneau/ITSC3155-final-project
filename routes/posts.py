# src/main_routes.py
from . import posts_bp
from flask import render_template, request, flash, redirect, session


@posts_bp.get('/new_post')
def new_post():
    return render_template('new_post.html')


@posts_bp.get('/post/<post_id>')
def post_detail(post_id):
    return render_template('post_detail.html', post_id=post_id)
