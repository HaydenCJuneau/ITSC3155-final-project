from werkzeug.security import check_password_hash
from src.models import db, User
import re

creators_dict = {
    'Hayden Juneau': {
        'description': '...',
        'image_src': '../static/images/hayden_headshot.jpg',
        'linkedin_link': '#',
        'github_link': '#'
    },
    'Oliver Brito': {
        'description': '...',
        'image_src': '',
        'linkedin_link': '#',
        'github_link': '#'
    },
    'Sasank Pagadala': {
        'description': '...',
        'image_src': '',
        'linkedin_link': '#',
        'github_link': '#'
    },
    'Safa Rasheed': {
        'description': '...',
        'image_src': '',
        'linkedin_link': '#',
        'github_link': '#'
    },
    'Yadhira Marcos': {
        'description': '...',
        'image_src': '',
        'linkedin_link': '#',
        'github_link': '#'
    },
    'Michael Gohn': {
        'description': '...',
        'image_src': '../static/images/michael_headshot.JPG',
        'linkedin_link': 'https://www.linkedin.com/in/michael-gohn-8a8963236/',
        'github_link': 'https://github.com/dashboard'
    },
}

def create_user(username, email, password_hash):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return 'Invalid email format'
    
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

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return 'Invalid email format'

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

def clear_db():
    db.session.remove()
    db.drop_all()
    db.create_all()