from src.backend import create_user, clear_db, delete_post
from src.models import db, Posts, Users
from datetime import datetime
import os

def generate_dummy_binary(size):
    return os.urandom(size)

def create_post(user):
    binary_data_size = 272 * 1024
    image_binary = generate_dummy_binary(binary_data_size)
    test_post = Posts(image=image_binary, title='test_title', timestamp=datetime.utcnow(), description='test_description', status='test_status', author_id=user.user_id)
    return test_post

def save_post_to_db(post):
    db.session.add(post)
    db.session.commit()

def test_delete_post(test_app):
    clear_db()

    create_user('test_name', 'test@test.com', 'password')
    test_user = Users.query.filter_by(username='test_name').first()

    test_post = create_post(test_user)
    save_post_to_db(test_post)

    result = delete_post(test_post.post_id)
    assert result == True

    deleted_post = db.session.query(Posts).get(test_post.post_id)
    assert deleted_post is None

