import os
from flask import Flask, render_template, redirect, request, session, flash, get_flashed_messages, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

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
def index():
    return render_template('index.html')

@app.get('/new_post')
def new_post():
    return render_template('new_post.html')


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

@app.route('/home/About')
def about():
    return render_template('about.html')


@app.get('/users/signup')
def user_signup():
    return render_template('signup.html')

@app.post('/users/signup')
def create_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users/login')

@app.get('/users/login')
def login_form():
    return render_template('login.html')

@app.post('/users/login')
def login_user():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.user_id
        return redirect('/users/profile')
    else:
        return 'Invalid username or password'

@app.get('/users/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/users/login')
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)

@app.get('/users/profile/edit')
def edit_profile_form():
    if 'user_id' not in session:
        return redirect('/users/login')
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('edit_profile.html', user=user)

@app.post('/users/profile/edit')
def edit_profile():
    if 'user_id' not in session:
        return redirect('/users/login')
    user_id = session['user_id']
    user = User.query.get(user_id)
    user.username = request.form['username']
    user.email = request.form['email']
    db.session.commit()
    return redirect('/users/profile')

@app.get('/users/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.post('/users/delete')
def delete_user():
    user_id = session.get('user_id')   
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        session.pop('user_id', None)
        flash('Your account has been successfully deleted')
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