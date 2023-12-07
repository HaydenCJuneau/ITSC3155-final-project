from src.models import Users, Posts, Comments, Likes, db

starter_user_id = None

def reset_db():
    global starter_user_id

    # Clear database
    Users.query.delete()
    Posts.query.delete()
    Comments.query.delete()
    Likes.query.delete()
    
    # Create dummy user
    starter_user = Users(username='test', email='test@test.com', password='test')
    db.session.add(starter_user)
    db.session.commit()

    # Save user id
    starter_user_id = starter_user.user_id
