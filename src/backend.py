from werkzeug.security import check_password_hash
from src.models import db, User

def create_user(username, email, password_hash):
    if User.query.filter_by(username=username).first():
        return 'Username already in use'
    if User.query.filter_by(email=email).first():
        return 'Email already in use'

    new_user = User(username=username, email=email, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return 'Success'

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def update_user_profile(user_id, username, email):
    user = get_user_by_id(user_id)
    existing_username = User.query.filter(User.user_id != user_id, User.username == username).first()
    existing_email = User.query.filter(User.user_id != user_id, User.email == email).first()

    if existing_username:
        return 'Username already in use'
    if existing_email:
        return 'Email already in use'
    
    user.username = username
    user.email = email
    db.session.commit()
    return 'Success'

def delete_user_account(user_id):
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def check_user_credentials(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user.password, password):
        return user
    return None
