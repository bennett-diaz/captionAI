import os
import logging
from dotenv import load_dotenv, find_dotenv
import captioner_gpt
import imgtotext_api

# Set up logging
logging.getLogger().handlers = []
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("myapp.log", mode="a")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
root_logger = logging.getLogger()
root_logger.addHandler(file_handler)
logger.info("*")

# Constants and configurations
load_dotenv(find_dotenv())
imgtotext_model = os.getenv("IMAGETOTEXT_MODEL_SMALL")
captioner_model = os.getenv("CAPTIONER_MODEL")
temp = float(os.getenv("TEMPERATURE"))
num_completions = int(os.getenv("NUM_COMPLETIONS"))

# Get image from user
# Temporary: hard-coded test URLs
sample_url1 = "https://images.unsplash.com/photo-1668554245790-bfdc72f0bb3d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2787&q=80"
sample_url2 = "https://images.unsplash.com/photo-1588180891305-0e6de022e52d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80"
sample_url3 = "https://images.unsplash.com/photo-1688890260360-e50f5b17ed55?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"

# Generate text summary of image
try:
    response = imgtotext_api.inference_url(imgtotext_model, sample_url3)
except Exception as e:
    logger.exception("An error occurred in imgtotext_api.inference_url: %s", str(e))

# Extract summary from API response
summary = response[0]["generated_text"]

# Formulate prompt for caption model
prompt = captioner_gpt.create_prompt(summary)

# Request captions from GPT
try:
    caption_list = captioner_gpt.generate_caption(
        captioner_model, prompt, temp, num_completions
    )
except Exception as e:
    logger.exception("An error occurred in captioner_gpt.generate_caption: %s", str(e))


# Display captions to the user
# Temporary: logs each caption in a numbered list
for i, caption in enumerate(caption_list, 1):
    caption_text = caption["message_content"].strip('"')
    logger.info(f"{i}: {caption_text}")
