from flask import Flask, render_template, redirect, request, jsonify
import os


app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')


@app.get('/profile')
def user_profile():
    return render_template('profile.html')


@app.get('/posts')
def new_post():
    return render_template('posts.html')


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