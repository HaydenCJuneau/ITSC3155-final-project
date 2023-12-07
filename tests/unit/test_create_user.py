from src.backend import create_user, clear_db

def test_create_user(test_app):
    clear_db()

    result = create_user('ryan', 'ryans@example.com', 'password')
    assert result == 'Success'

def test_create_user_invalid_email(test_app):
    clear_db()

    result = create_user('ryan', '90euj09pjpiso', 'password')
    assert result == 'Invalid email format'

def test_create_user_duplicate_email(test_app):
    clear_db()
   
    create_user('ryan', 'ryans@example.com', 'password')
    result = create_user('newuser', 'ryans@example.com', 'password')
    assert result == 'Email already in use'

