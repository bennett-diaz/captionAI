import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv, find_dotenv
import json

# import files from parent directory
import sys
sys.path.append('..')
from captionAI import captioner_gpt
from captionAI import imgtotext_api

app = Flask(__name__, static_url_path='/static')

# Constants and configurations
load_dotenv(find_dotenv())
imgtotext_model = os.getenv("IMGTXT_MODEL_GITBASE")
captioner_model = os.getenv("CAPTIONER_MODEL_GPT")
temp = float(os.getenv("TEMPERATURE"))
num_completions = int(os.getenv("NUM_COMPLETIONS"))

# Function to process the image and generate captions
def process_image(image_url):
    # Generate text summary of the image
    response = imgtotext_api.inference_url(imgtotext_model, image_url)
    summary = response[0]["generated_text"]

    # Formulate prompt for the caption model
    prompt = captioner_gpt.create_prompt(summary)

    # Request captions from GPT
    caption_list = captioner_gpt.generate_caption(captioner_model, prompt, temp, num_completions)
    return caption_list

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    if request.method == 'POST':
        image_url = request.form.get('image_url')

        if image_url:
            try:
                # Redirect to the loading page with the image URL
                return redirect(url_for('loading_page', image_url=image_url))

            except Exception as e:
                return render_template('landing.html', error_message='Failed to process the image.')

    return render_template('landing.html', error_message=None)

@app.route('/loading')
def loading_page():
    # Get the image URL from the inference parameters
    image_url = request.args.get('image_url')

    return render_template('loading.html', image_url=image_url)

@app.route('/process_image', methods=['POST'])
def process_image_route():
    if request.method == 'POST':
        data = request.get_json()
        image_url = data.get('image_url')

        if image_url:
            try:
                # Process the image and generate captions
                caption_list = process_image(image_url)

                # Return the captions as a JSON response
                return jsonify({'captions': caption_list})

            except Exception as e:
                return jsonify({'error': 'Failed to process the image.'}), 500

    return jsonify({'error': 'Invalid request.'}), 400

@app.route('/results')
def results_page():
    # Get the image URL and captions list from the inference parameters
    image_url = request.args.get('image_url')
    caption_list = request.args.get('caption_list')

    if image_url and caption_list:
        # Parse the JSON captions list
        caption_list = json.loads(caption_list)

        return render_template('results.html', image_url=image_url, caption_list=caption_list)

    return jsonify({'error': 'Invalid request.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
    # c = process_image("https://images.unsplash.com/photo-1689758410578-574c8f9eff2b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80")
    # print(c)
