from src.user_utils import create_user, clear_db
from src.models import db, Posts, Users, Likes
# May want to delete these imports after refining. This test is in a temporary state
from datetime import datetime
import os
from random import random

def generate_dummy_binary(size):
    return os.urandom(size)

def save_like_to_db(like):
    db.session.add(like)
    db.session.commit()

def test_save_like(test_app):
    clear_db()

    # Create test user and save to db
    create_user('test_name', 'test@test.com', 'password')
    test_user = Users.query.filter_by(username='test_name').first()

    # Create test post and save to db
    binary_data_size = 272 * 1024
    image_binary = generate_dummy_binary(binary_data_size)
    test_post = Posts(image=image_binary, title='test_title', timestamp=datetime.utcnow(), description='test_description', status='test_status', author_id=test_user.user_id)
    db.session.add(test_post)
    db.session.commit()

    # Create test comment and save to db
    test_like = Likes(user_id=test_user.user_id, post_id=test_post.post_id)
    save_like_to_db(test_like)

    # Assert test post is in the db
    assert db.session.query(Likes).get(test_like.like_id).post_id == test_post.post_id
    assert db.session.query(Likes).get(test_like.like_id).user_id == test_user.user_id

