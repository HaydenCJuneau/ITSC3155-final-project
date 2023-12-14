<<<<<<< HEAD
from src.user_utils import create_user, clear_db
=======
from src.backend import create_user, clear_db, generate_dummy_binary, save_item_to_db
>>>>>>> profile-posts
from src.models import db, Posts, Users
# May want to delete these imports after refining. This test is in a temporary state
from datetime import datetime

def test_save_post(test_app):
    clear_db()

    # Create test user and save to db
    create_user('test_name', 'test@test.com', 'password')
    test_user = Users.query.filter_by(username='test_name').first()

    # Create test post and save to db
    binary_data_size = 272 * 1024
    image_binary = generate_dummy_binary(binary_data_size)
    test_post = Posts(image=image_binary, title='test_title', timestamp=datetime.utcnow(), description='test_description', status='test_status', author_id=test_user.user_id)
    save_item_to_db(test_post)

    # Assert test post is in the db
    assert db.session.query(Posts).get(test_post.post_id).image is not None
    assert db.session.query(Posts).get(test_post.post_id).title == 'test_title'
    assert db.session.query(Posts).get(test_post.post_id).timestamp is not None
    assert db.session.query(Posts).get(test_post.post_id).description == 'test_description'
    assert db.session.query(Posts).get(test_post.post_id).status == 'test_status'
    assert db.session.query(Posts).get(test_post.post_id).author_id == test_user.user_id

