import os
from flask import Flask, render_template, redirect, request, session, flash, get_flashed_messages, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.backend import create_user, check_user_credentials, update_user_profile, delete_user_account, get_user_by_id

from src.models import db, User

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET')

app.config['SQLALCHEMY_DATABASE_URI'] = \
f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.get('/')
def home():
    return render_template('home.html')

@app.get('/create_post')
def new_post():
    return render_template('create_post.html')


@app.get('/post/<post_id>')
def post_detail(post_id):
    return render_template('post_detail.html', post_id=post_id)


@app.get('/search')
def search():
    query = request.args.get('q')
    return render_template('search.html', query=query)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts')
def posts():
    return render_template('posts.html')


def is_logged_in():
    return 'user_id' in session

@app.get('/users/signup')
def user_signup():
    if is_logged_in():
        flash('You are already logged in.')
        return redirect('/')
    return render_template('signup.html')

@app.post('/users/signup')
def signup_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    result = create_user(username, email, hashed_password)
    if result == 'Success':
        flash('Account successfully created')
        return redirect('/')
    else:
        flash(result) 
        return redirect('/users/signup')

@app.get('/users/login')
def login_form():
    if is_logged_in():
        flash('You are already logged in.')
        return redirect('/')
    return render_template('login.html')

@app.post('/users/login')
def login_user():
    email = request.form['email']
    password = request.form['password']
    user = check_user_credentials(email, password)
    if user:
        session['user_id'] = user.user_id
        session['username'] = user.username
        return redirect('/')
    else:
        flash('Invalid email or password')
        return redirect('/')

@app.get('/users/profile')
def profile():
    if not is_logged_in():
        flash('Please log in to access your profile.')
        return redirect('/')
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    return render_template('profile.html', user=user)

@app.get('/users/profile/edit')
def edit_profile_form():
    if not is_logged_in():
        flash('Please log in to edit your profile.')
        return redirect('/')
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    return render_template('edit_profile.html', user=user)

@app.post('/users/profile/edit')
def edit_profile():
    if 'user_id' not in session:
        flash('Please log in to edit your profile')
        return redirect('/')
    user_id = session['user_id']
    username = request.form['username']
    email = request.form['email']

    result = update_user_profile(user_id, username, email)
    if result == 'Success':
        session['username'] = username
        flash('Profile updated successfully')
        return redirect('/users/profile')
    else:
        flash(result)  
        return redirect('/users/profile/edit')

@app.get('/users/logout')
def logout():
    if not is_logged_in():
        flash('You are not logged in.')
        return redirect('/')
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been successfully logged out.')
    return redirect('/')

@app.post('/users/delete')
def delete_user():
    if not is_logged_in():
        flash('Please log in to delete your account.')
        return redirect('/')
    user_id = session['user_id']
    if delete_user_account(user_id):
        session.clear()
        flash('Your account has been successfully deleted.')
    else:
        flash('User could not be found')
    return redirect('/')




@app.route('/home/Canvas')
def canvas():
    return render_template('canvas.html')


##TEST FOR JASONIFY##
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded.png')
    file.save(filename)

    return jsonify({'success': True, 'message': 'File uploaded successfully'})