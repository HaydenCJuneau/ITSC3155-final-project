import requests
import base64
from io import BytesIO
from PIL import Image
from random import randint

TOKEN = "key-dInP5mSzWiNyBfe4BqDWD5NAz62Wf8PMVd9FCsBiziCzORoBtLHKmjLbEy4DLqZIRFntEZaITvkDUS0bqWiK6tBO4brgY5k"


def check_balance():
    import requests

    url = "https://api.getimg.ai/v1/account/balance"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(url, headers=headers)

    print(response.text)


def decode_image(base64_string: str):
    image_data = base64.b64decode(base64_string)
    image_stream = BytesIO(image_data)
    image = Image.open(image_stream)
    image.save(f'./uploads/output.jpg', 'JPEG')


def invert_ctrl_image(img_path: str):
    image = Image.open(img_path)
    inverted = Image.eval(image, lambda x: 255 - x)
    inverted.save(img_path, "PNG")


def encode_ctrl_image(img_path: str) -> str:
    # Encode the image into a string
    try: 
        with open(img_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read())
            return encoded_string.decode()
    except:
        print("An error occured during encoding of control image!")
        exit()


def request_image():
    url = "https://api.getimg.ai/v1/stable-diffusion/controlnet"
    controlImage = "./uploads/input.png"

    invert_ctrl_image(controlImage)

    encoded_string = encode_ctrl_image(controlImage)

    

    payload = {
        "model": "icbinp-seco",
        "controlnet": "scribble-1.1",
        "prompt": "(fruit), realistic photo of a futuristic orange with cyborg alien arms and legs and human eyes",
        "negative_prompt": "((nsfw)), bad quality, cartoon",
        "width": 512, 
        "height": 512, 
        "steps": 20, 
        "guidance": 5,
        "scheduler": "dpmsolver++",
        "image": encoded_string
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    response = requests.post(url, json=payload, headers=headers)

    #print(response.text)

    # Decode and save the image
    json_response = response.json()

    decode_image(json_response["image"])


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
    


if __name__ == "__main__":
    # request_image()
    # invert_ctrl_image("./uploads/input.png")
    check_balance()