from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Posts(db.Model):
    __tablename__ = 'posts'
    
    post_id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(255), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), \
                            nullable=False)
    author = db.relationship('Users', backref='posts')

class Comments(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), \
                        nullable=False)
    post = db.relationship('Posts', backref='comments')

    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), \
                        nullable=False)
    author = db.relationship('Users', backref='comments')

class Likes(db.Model):
    __tablename__ = 'likes'

    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), \
                        nullable=False)
    user = db.relationship('Users', backref='likes')

    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), \
                        nullable=False)
    post = db.relationship('Posts', backref='likes')