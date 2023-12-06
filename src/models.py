from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return f'Users({self.user_id}, {self.username}, {self.email}, {self.password})'

class Posts(db.Model):
    __tablename__ = 'posts'
    
    post_id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(255), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), \
                            nullable=False)
    author = db.relationship('Users', backref='posts')

    def __repr__(self) -> str:
        return f'Posts({self.post_id}, {self.image}, {self.title}, {self.timestamp}, {self.description}, {self.status}, {self.author_id})'

class Comments(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), \
                        nullable=False)
    post = db.relationship('Posts', backref='comments')

    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), \
                        nullable=False)
    author = db.relationship('Users', backref='comments')

    def __repr__(self) -> str:
        return f'Comments({self.comment_id}, {self.text}, {self.post_id}, {self.author_id}'

class Likes(db.Model):
    __tablename__ = 'likes'

    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), \
                        nullable=False)
    user = db.relationship('Users', backref='likes')

    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), \
                        nullable=False)
    post = db.relationship('Posts', backref='likes')

    def __repr__(self) -> str:
        return f'Likes({self.like_id}, {self.user_id}, {self.post_id}'