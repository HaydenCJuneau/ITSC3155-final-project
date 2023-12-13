from src.user_utils import get_user_by_email, clear_db

def test_delete_user_successful(test_app):
    clear_db()

    test_app.post('/users/signup', data={
        'username': 'ryan',
        'email': 'ryans@gmail.com',
        'password': 'password'
    }, follow_redirects=True)

    test_app.post('/users/login', data={
        'email': 'ryans@gmail.com',
        'password': 'password'
    }, follow_redirects=True)

    with test_app.session_transaction() as sess:
        user = get_user_by_email('ryans@gmail.com')
        sess['user_id'] = user.user_id

    response = test_app.post('/users/delete', follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert 'Your account has been successfully deleted' in data

def test_delete_user_not_logged_in(test_app):

    response = test_app.post('/users/delete', follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert 'Please log in to delete your account' in data