import os
import requests
from dotenv import load_dotenv, find_dotenv
import json

# constants and configurations
load_dotenv(find_dotenv())
token = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {token}"}
LOAD_URL = "https://api-inference.huggingface.co/models/"


# run inference on HuggingFace API and return image summary as list of dicts
# API will cache result by default, forcing model output to be deterministic
def query_file(model_id, filename):
    api_url = LOAD_URL + model_id

    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(api_url, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


def query_url(model_id, image_url):
    api_url = "https://api-inference.huggingface.co/models/" + model_id

    # send a GET request to URL and get imgage in binary format (i.e. bytes)
    image_data = requests.get(image_url).content
    response = requests.post(api_url, headers=headers, data=image_data)
    listdict = response.json()
    return listdict[0]["generated_text"]
