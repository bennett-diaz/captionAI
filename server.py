import os
from dotenv import load_dotenv, find_dotenv
import captioner_gpt
import imgtotext_api
import pprint

# constants and configurations
load_dotenv(find_dotenv())
imgtotext_model = os.getenv("IMAGETOTEXT_MODEL_LARGE")
captioner_model = os.getenv("CAPTIONER_MODEL")
temp = float(os.getenv("TEMPERATURE"))
num_completions = int(os.getenv("NUM_COMPLETIONS"))

# get image from user
# temporary: hard-coded test URLs
sample_url1 = "https://images.unsplash.com/photo-1668554245790-bfdc72f0bb3d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2787&q=80"
sample_url2 = "https://images.unsplash.com/photo-1588180891305-0e6de022e52d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80"
sample_url3 = "https://images.unsplash.com/photo-1688890260360-e50f5b17ed55?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"

# generate text summary of image
response = imgtotext_api.query_url(imgtotext_model, sample_url3)

# extract summary from API response
summary = response[0]["generated_text"]

# formulate prompt for caption model
prompt = captioner_gpt.create_prompt(summary)

# request captions from GPT
caption_list = captioner_gpt.generate_caption(
    captioner_model, prompt, temp, num_completions
)


# display captions to the user
# temporary: prints each caption in a numbered list
for i, caption in enumerate(caption_list, 1):
    print(i, caption["message_content"].strip('"'))
