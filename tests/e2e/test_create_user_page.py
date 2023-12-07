def test_create_user_page(test_app):
    
    response = test_app.get('/users/signup')
    assert response.status_code == 200
    assert "Sign Up" in response.data.decode('utf-8')

def test_create_user_success(test_app):

    user_data = {
        "username": "ryan",
        "email": "ryans@gmail.com",
        "password": "password"
    }

    response = test_app.post('/users/signup', data=user_data, follow_redirects=True)
    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert "Account successfully created" in data
    assert "Login" in data

def test_create_user_with_existing_username(test_app):
    
    user_data = {
        "username": "ryan",  
        "email": "jimb@gmail.com",
        "password": "password"
    }
    response = test_app.post('/users/signup', data=user_data, follow_redirects=True)
    data = response.data.decode('utf-8')
    assert "Username already in use" in data
