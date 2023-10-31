from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup_page.html')


@app.route('/login')
def login():
    return render_template('login_page.html')


@app.route('/profile/<username>')
def user_profile(username):
    return render_template('user_profile.html', username=username)


@app.route('/post/new')
def new_post():
    return render_template('post_creation.html')


@app.route('/post/<post_id>')
def post_detail(post_id):
    return render_template('post_detail.html', post_id=post_id)


@app.route('/post/<post_id>/edit')
def edit_post(post_id):
    return render_template('edit_post.html', post_id=post_id)


@app.route('/category/<category_name>')
def posts_by_category(category_name):
    
    return render_template('posts_by_category.html', category_name=category_name)


@app.route('/search')
def search():
    query = request.args.get('q')
    return render_template('search_results.html', query=query)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')