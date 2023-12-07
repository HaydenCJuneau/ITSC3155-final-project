from src.backend import create_user, update_user_profile, clear_db

def test_update_user_valid_data(test_app):
    clear_db()
    
    create_user('jumper', 'jumper@gmail.com', 'password')
    result = update_user_profile(1, 'jumper1', 'jumper1@gmail.com')
    assert result == 'Success'

def test_update_user_duplicate_username(test_app):
    clear_db()
    
    create_user('ryan', 'ryans@gmail.com', 'password')
    create_user('jim', 'jimb@gmail.com', 'password')
    result = update_user_profile(2, 'ryan', 'jimb@gmail.com')
    assert result == 'Username already in use'

def test_update_user_duplicate_email(test_app):
    clear_db()
    
    create_user('ryan', 'ryans@gmail.com', 'password')
    create_user('jim', 'jimb@gmail.com', 'password')
    result = update_user_profile(2, 'jim', 'ryans@gmail.com')
    assert result == 'Email already in use'

def test_update_user_invalid_email(test_app):
    clear_db()
    
    create_user('ryan', 'ryans@gmail.com', 'password')
    result = update_user_profile(1, 'ryan', 'jioudshjouashj')
    assert result == 'Invalid email format'
