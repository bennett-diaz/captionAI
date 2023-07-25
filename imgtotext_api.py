import os
import json
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
token = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {token}"}
LOAD_URL = "https://api-inference.huggingface.co/models/"


# run inference on HuggingFace API and return image summary as list of dicts
# API will cache result by default, forcing model output to be deterministic
def inference_file(model_id, filename):
    api_url = LOAD_URL + model_id

    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(api_url, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


def inference_url(model_id, image_url):
    try:
        api_url = "https://api-inference.huggingface.co/models/" + model_id

        # get image data in binary format (i.e. bytes)
        img = requests.get(image_url, timeout=8000).content

        response = requests.post(api_url, headers=headers, data=img, timeout=8000)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        error_message = (
            f"HTTPError {e.response.status_code}: {e.response.content.decode('utf-8')}"
        )
        raise Exception(error_message)

    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")
