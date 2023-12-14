from src.user_utils import create_user, clear_db
from src.models import db, Posts, Users
# May want to delete these imports after refining. This test is in a temporary state
from datetime import datetime

def create_post(user):
    binary_data_size = 272 * 1024
    image_binary = generate_dummy_binary(binary_data_size)
    test_post = Posts(image=image_binary, title='test_title', timestamp=datetime.utcnow(), description='test_description', status='test_status', author_id=user.user_id)
    return test_post

def test_update_post(test_app):
    clear_db()
    create_user('test_name', 'test@test.com', 'password')
    test_user = Users.query.filter_by(username='test_name').first()
    test_post = create_post(test_user)
    save_item_to_db(test_post)

    test_post.title = 'new_title'
    test_post.description = 'new_description'
    test_post.status = 'new_status'

    db.session.commit()

    assert db.session.query(Posts).get(test_post.post_id).title == 'new_title'
    assert db.session.query(Posts).get(test_post.post_id).description == 'new_description'
    assert db.session.query(Posts).get(test_post.post_id).status == 'new_status'


