import os
from src.user_utils import creators_dict
from flask import Flask, render_template, request
from src.models import db

# Import and register environment variables
from dotenv import load_dotenv
load_dotenv()

# Create new app object
app = Flask(__name__)


# Import and register blueprints
from routes import users_bp, posts_bp

app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)

# Register secret for session management
app.secret_key = os.getenv('SECRET')

# Register DB connection settings
app.config['SQLALCHEMY_DATABASE_URI'] = \
f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize app
db.init_app(app)


# - - - Below are basic naviation routes - - -
# Any specific API or nav routes that can be sectioned off into modules should be
@app.get('/')
def home():
    return render_template('home.html')


@app.get('/search')
def search():
    query = request.args.get('q')
    return render_template('search.html', query=query)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html', creators_dict = creators_dict)


if __name__ == '__main__':
    app.run(debug=True)
