from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')


@app.get('/profile')
def user_profile():
    return render_template('profile.html')


@app.get('/posts')
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