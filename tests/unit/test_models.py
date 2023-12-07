from ..utils import reset_db, starter_user_id
from src.models import Posts, db
from datetime import datetime
import os
from random import random

def generate_dummy_binary(size):
    return os.urandom(size)

def test_create_post(test_client):
    reset_db()

    binary_data_size = 272 * 1024

    image_binary = generate_dummy_binary(binary_data_size)

    new_post = Posts(image=image_binary, title='test_title', timestamp=datetime.utcnow(), description='test_description', status='test_status', author_id=starter_user_id)
    db.session.add(new_post)
    db.session.commit()

    assert db.session.query(Posts).get(new_post.post_id).title == 'test_title'