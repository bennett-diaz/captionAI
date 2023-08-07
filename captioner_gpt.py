import os
from dotenv import load_dotenv, find_dotenv
import openai

# constants and configurations
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")


# formulate prompt based on requirements for OpenAI Chat endpoint
def create_prompt(summary):
    prompt = [
        {
            "role": "user",
            "content": "Generate a short instagram caption for this image: " + summary,
        }
    ]
    return prompt


# call API and return a list of dictionaries: 1 dictionary per caption
def generate_caption(mod, msg, temp, num_completions):
    try:
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

    except Exception as err:
        raise err
