# post_utils.py
# This file stores helper methods for image generation and post editing
import requests, os, base64
from datetime import datetime
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from src.models import db, Posts, Users, Comments, Likes
from sqlalchemy import union

load_dotenv()
TOKEN = os.getenv('API_KEY')
API_URL = "https://api.getimg.ai/v1/stable-diffusion/controlnet"
IMG_SIZE = 512

# Post DB functions 
def create_post(imageData: str, title: str, description: str, author) -> Posts|None:
    try:
        newPost = Posts(image=imageData.encode(), title=title, description=description, \
            timestamp=datetime.utcnow(), status='ready', author_id=author)
        db.session.add(newPost)
        db.session.commit()
        return newPost
    except Exception as e:
        print(f'A problem occurred saving post to db: {e}')
        return None


def get_all_posts():
    try:
        return Posts.query.all()
    except Exception as e:
        print(f'A problem occurred getting all posts from db: {e}')
        return None


def search_post(search: str):
    try:
        titleQuery = Posts.query.filter(Posts.title.ilike(f'%{search}%')).all()
        return titleQuery
    except Exception as e:
        print(f'A problem occurred searching for posts: {e}')


def get_post_by_id(post_id):
    try:
        return Posts.query.get(post_id)
    except Exception as e:
        print(f'A problem occurred getting post from db: {e}')
        return None

# Image pipeline functions

def check_balance():
    import requests

    url = "https://api.getimg.ai/v1/account/balance"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(url, headers=headers)

    print(response.text)


def parse_models():
    url = "https://api.getimg.ai/v1/models?family=stable-diffusion&pipeline=controlnet"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(url, headers=headers)

    json = response.json()
    filtered = [{'id': x['id'], 'name': x['name']} for x in json]
    [print(x) for x in filtered]


def decode_image(base64_string: str, file_name: str, ext: str = 'JPEG'):
    image_data = base64.b64decode(base64_string)
    image_stream = BytesIO(image_data)
    image = Image.open(image_stream)
    image.save(file_name, ext)
    image_stream.close()
    image.close()


def invert_ctrl_image(base64_string: str) -> str:
    # Decode the base64 string
    image_data = base64.b64decode(base64_string)
    image_stream = BytesIO(image_data)

    image = Image.open(image_stream)

    inverted = Image.eval(image, lambda x: 255 - x)

    inverted_stream = BytesIO()
    inverted.save(inverted_stream, format='JPEG')
    inverted_data = inverted_stream.getvalue()

    inverted_base64 = base64.b64encode(inverted_data).decode('utf-8')

    image_stream.close()
    image.close()
    inverted_stream.close()
    return inverted_base64


def encode_ctrl_image(img_path: str) -> str:
    # Encode the image into a string
    try: 
        with open(img_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read())
            return encoded_string.decode()
    except:
        print("An error occured during encoding of control image!")
        exit()


def queue_image_generation(post_id: int, user_prompt: str, ctrl_image: str):
    payload = {
        "model": "icbinp-seco",
        "controlnet": "scribble-1.1",
        "prompt": f"(fruit), realistic photo, photograph, {user_prompt}",
        # Since model can be used for nsfw and favors it heavily when positively prompted
        # put extra negative emphasis on nsfw prompts.
        "negative_prompt": "((nsfw)), (nudity), (human), (human body), (woman), unrealistic, bad quality, cartoon",
        "width": IMG_SIZE, 
        "height": IMG_SIZE, 
        "steps": 20, 
        "guidance": 5,
        "scheduler": "dpmsolver++",
        "image": ctrl_image
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        print(f'Generation Call Failed! \nMessage:{response.text}')

    # Decode and save the image
    json_response = response.json()

    decode_image(json_response["image"], f'./uploads/output.jpg')
    return json_response["image"]


def delete_post_by_id(post_id, user_id):
    post = Posts.query.get(post_id)
    if post is None:
        return 'Post not found.'

    if post.author_id != user_id:
        return 'You can only delete your own posts.'
    
    Likes.query.filter_by(post_id=post_id).delete()
    Comments.query.filter_by(post_id=post_id).delete()

    db.session.delete(post)
    db.session.commit()
    return 'Post deleted successfully.'


def clear_db():
    db.session.remove()
    db.drop_all()
    db.create_all()


def create_comment(post_id, user_id, text):
    new_comment = Comments(post_id=post_id, author_id=user_id, text=text)
    db.session.add(new_comment)
    db.session.commit()
    return new_comment


def get_comment_by_id(comment_id):
    return Comments.query.get(comment_id)


def update_comment(comment_id, new_text):
    comment = get_comment_by_id(comment_id)
    if comment:
        comment.text = new_text
        db.session.commit()
        return True
    return False


def delete_comment(comment_id):
    comment = get_comment_by_id(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return True
    return False


def get_comments_for_post(post_id):
    try:
        return Comments.query.filter_by(post_id=post_id).all()
    except Exception as e:
        print(f'Error getting comments for post {post_id}: {e}')
        return []


def like_post(user_id, post_id):
    existing_like = Likes.query.filter_by(user_id=user_id, post_id=post_id).first()
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        return 'unliked'
    else:
        new_like = Likes(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        return 'liked'


def check_user_like(user_id, post_id) -> bool:
    try:
        return Likes.query.filter_by(user_id=user_id, post_id=post_id).first() is not None
    except Exception as e:
        print(f'Error checking user like: {e}')
        return False


def get_like_count(post_id):
    return Likes.query.filter_by(post_id=post_id).count()
