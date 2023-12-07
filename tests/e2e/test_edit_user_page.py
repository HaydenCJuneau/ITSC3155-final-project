from src.backend import get_user_by_email, clear_db

def test_access_edit_profile_page_not_logged_in(test_app):
    
    response = test_app.get('/users/profile/edit', follow_redirects=True)
    assert response.status_code == 200
    assert "Please log in" in response.data.decode('utf-8')

def test_access_edit_profile_page_logged_in(test_app):
    
    with test_app.session_transaction() as sess:
        sess['user_id'] = 1  

    response = test_app.get('/users/profile/edit')
    assert response.status_code == 200
    assert "Edit Profile" in response.data.decode('utf-8')

def test_update_user_profile(test_app):
    
    test_app.post('/users/signup', data={
        'username': 'ryan',
        'email': 'ryans@gmail.com',
        'password': 'password'
    }, follow_redirects=True)

    user_data = {
        "username": "jim",
        "email": "jimb@gmail.com"
    }

    with test_app.session_transaction() as sess:
        user = get_user_by_email('ryans@gmail.com')
        sess['user_id'] = user.user_id

    response = test_app.post('/users/profile/edit', data=user_data, follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200


def test_update_user_profile_with_existing_email(test_app):
    clear_db()

    test_app.post('/users/signup', data={
        'username': 'ryan',
        'email': 'ryans@gmail.com',
        'password': 'password'
    }, follow_redirects=True)

    test_app.post('/users/signup', data={
        'username': 'jimbo',
        'email': 'jimbo@gmail.com',
        'password': 'password'
    }, follow_redirects=True)

    user_data = {
        "username": "ryan",
        "email": "jimbo@gmail.com"
    }

    with test_app.session_transaction() as sess:
        user = get_user_by_email('ryans@gmail.com')
        sess['user_id'] = user.user_id

    response = test_app.post('/users/profile/edit', data=user_data, follow_redirects=True)
    data = response.data.decode('utf-8')
    assert "Email already in use" in data

def test_update_user_profile_invalid_email(test_app):

    user_data = {
        "username": "himmy",
        "email": "djiojsopjdap0aww"
    }

    with test_app.session_transaction() as sess:
        sess['user_id'] = 1  

    response = test_app.post('/users/profile/edit', data=user_data, follow_redirects=True)
    data = response.data.decode('utf-8')
    assert "Invalid email format" in data