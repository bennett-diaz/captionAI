import os
from dotenv import load_dotenv, find_dotenv
import openai

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")


# format prompt to conform to GPT API requirements
def create_prompt(summary):
    messages = [
        {
            "role": "user",
            "content": "Generate a short instagram caption for this image: " + summary,
        }
    ]
    return messages


# call API endpoint and return a list of dictionaries
# API request paramters are defined in the .env file
def generate_caption(mod, msg, temp=0.7, num_completions=1):
    completion = openai.ChatCompletion.create(
        model=mod,
        messages=msg,
        temperature=temp,
        n=num_completions,
    )

    caption_list = []
    for choice in completion.choices:
        choice_data = {
            "finish_reason": choice["finish_reason"],
            "index": choice["index"],
            "message_content": choice["message"]["content"],
            "created": completion.created,
            "model": completion.model,
        }
        caption_list.append(choice_data)
    return caption_list


if __name__ == "__main__":
    print("You are only running" + __file__ + "and not importing it.")
