import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv, find_dotenv
import json

# import files from parent directory
import sys
sys.path.append('..')
from captionAI import captioner_gpt
from captionAI import imgtotext_api


app = Flask(__name__)

# Constants and configurations
load_dotenv(find_dotenv())
imgtotext_model = os.getenv("IMAGETOTEXT_MODEL_LARGE")
captioner_model = os.getenv("CAPTIONER_MODEL")
temp = float(os.getenv("TEMPERATURE"))
num_completions = int(os.getenv("NUM_COMPLETIONS"))

# Function to process the image and generate captions
def process_image(image_url):
    # Generate text summary of the image
    summary = imgtotext_api.query_url(imgtotext_model, image_url)

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
    # Get the image URL from the query parameters
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
    # Get the image URL and captions list from the query parameters
    image_url = request.args.get('image_url')
    caption_list = request.args.get('caption_list')

    if image_url and caption_list:
        # Parse the JSON captions list
        caption_list = json.loads(caption_list)

        return render_template('results.html', image_url=image_url, caption_list=caption_list)

    return jsonify({'error': 'Invalid request.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
