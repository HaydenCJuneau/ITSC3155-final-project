# post_utils.py
# This file stores helper methods for image generation and post editing
import requests, os, base64
from datetime import datetime
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from src.models import db, Posts, Users

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
