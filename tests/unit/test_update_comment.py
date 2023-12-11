from src.backend import create_user, clear_db, generate_dummy_binary, save_item_to_db
from src.models import db, Posts, Users, Comments
# May want to delete these imports after refining. This test is in a temporary state
from datetime import datetime


def create_post(user):
    binary_data_size = 272 * 1024
    image_binary = generate_dummy_binary(binary_data_size)
    test_post = Posts(image=image_binary, title='test_title', timestamp=datetime.utcnow(), description='test_description', status='test_status', author_id=user.user_id)
    return test_post

def create_comment(user, post):
    test_comment = Comments(text='test_text', post_id=post.post_id, author_id=user.user_id)
    return test_comment

def test_update_comment(test_app):
    clear_db()

    create_user('test_name', 'test@test.com', 'password')
    test_user = Users.query.filter_by(username='test_name').first()

    test_post = create_post(test_user)
    save_item_to_db(test_post)

    test_comment = create_comment(test_user, test_post)
    save_item_to_db(test_comment)

    test_comment.text = 'new_text'

    db.session.commit()

    assert db.session.query(Comments).get(test_post.post_id).text == 'new_text'
