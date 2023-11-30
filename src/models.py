from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class Post(db.Model):
    __tablename__ = 'post'
    
    post_id = db.Column(db.Integer, primary_key=True)
    num_likes = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    caption = db.Column(db.String(255), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), \
                            nullable=False)
    author = db.relationship('User', backref='posts')

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    num_likes = db.Column(db.Integer, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), \
                        nullable=False)
    post = db.relationship('Post', backref='comments')

    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), \
                        nullable=False)
    author = db.relationship('User', backref='comments')