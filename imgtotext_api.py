import os
import json
import time
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
    response = requests.post(api_url, headers=headers, data=data, timeout=8)
    return json.loads(response.content.decode("utf-8"))


def inference_url(model_id, image_url):
    try:
        api_url = "https://api-inference.huggingface.co/models/" + model_id

        # Get image data in binary format (i.e. bytes)
        img = requests.get(image_url, timeout=8).content

        response = requests.post(api_url, headers=headers, data=img, timeout=8)
        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as err:
        current_filename = os.path.basename(__file__)
        error_message = (
            f"HTTPError in {current_filename}: {err.response.status_code}: {err.response.content.decode('utf-8')}"
        )

        # path if model has not yet deployed to Inference API
        if "estimated_time" in err.response.json():
            load_time = err.response.json()["estimated_time"]
            retry_time = load_time / 2
            retries = 5
            retry = 0
            while retry < retries:
                try:
                    time.sleep(retry_time)
                    response = requests.post(
                        api_url, headers=headers, data=img, timeout=load_time
                    )
                    response.raise_for_status()
                    return response
                except requests.exceptions.HTTPError:
                    retry += 1

            raise Exception(f"Model did not become available within {retries} retries.")

        else:
            raise Exception(error_message)
