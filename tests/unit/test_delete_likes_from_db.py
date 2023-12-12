from src.backend import create_user, clear_db, delete_likes
from src.models import db, Posts, Users, Likes
from datetime import datetime
import os

def generate_dummy_binary(size):
    return os.urandom(size)

def save_like_to_db(like):
    db.session.add(like)
    db.session.commit()

def test_delete_like(test_app):
    clear_db()
    create_user('test_name', 'test@test.com', 'password')
    test_user = Users.query.filter_by(username='test_name').first()

    binary_data_size = 272 * 1024
    image_binary = generate_dummy_binary(binary_data_size)
    test_post = Posts(image=image_binary, title='test_title', timestamp=datetime.utcnow(), description='test_description', status='test_status', author_id=test_user.user_id)
    db.session.add(test_post)
    db.session.commit()

    test_like = Likes(user_id=test_user.user_id, post_id=test_post.post_id)
    save_like_to_db(test_like)

    result = delete_likes(test_like.like_id)
    assert result == True

    deleted_like = db.session.query(Likes).get(test_like.like_id)

    assert deleted_like is None
