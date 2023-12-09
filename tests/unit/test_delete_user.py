from src.user_utils import create_user, clear_db, delete_user_account, get_user_by_id

def test_delete_user_account(test_app):
    clear_db()
    
    create_user('ryan', 'ryans@gmail.com', 'password')
    user = get_user_by_id(1)  
    result = delete_user_account(user.user_id)
    assert result == True


def test_delete_non_existent_user(test_app):
    clear_db()

    result = delete_user_account(999)  
    assert result == False

def test_user_removal_from_database(test_app):
    clear_db()
    
    create_user('ryan', 'ryans@gmail.com', 'password')
    user = get_user_by_id(1)  
    delete_user_account(user.user_id)
    deleted_user = get_user_by_id(user.user_id)
    assert deleted_user is None
