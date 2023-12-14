<<<<<<< HEAD
from src.user_utils import create_user, clear_db
=======
from src.backend import create_user, clear_db, generate_dummy_binary, save_item_to_db
>>>>>>> profile-posts
from src.models import db, Posts, Users, Comments
# May want to delete these imports after refining. This test is in a temporary state
from datetime import datetime

def test_save_comment(test_app):
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
    test_comment = Comments(text='test_text', post_id=test_post.post_id, author_id=test_user.user_id)
    save_item_to_db(test_comment)

    # Assert test post is in the db
    assert db.session.query(Comments).get(test_comment.comment_id).text == 'test_text'
    assert db.session.query(Comments).get(test_comment.comment_id).post_id == test_post.post_id
    assert db.session.query(Comments).get(test_comment.comment_id).author_id == test_user.user_id

