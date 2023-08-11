import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv, find_dotenv
import json

# import files from parent directory
import sys

sys.path.append("..")
from captionAI import captioner_gpt
from captionAI import imgtotext_api

app = Flask(__name__, static_url_path="/static")

load_dotenv(find_dotenv())
imgtotext_model = os.getenv("IMGTXT_MODEL_GITBASE")
captioner_model = os.getenv("CAPTIONER_MODEL_GPT")
temp = float(os.getenv("TEMPERATURE"))
num_completions = int(os.getenv("NUM_COMPLETIONS"))


@app.route("/", methods=["GET", "POST"])
def landing_page():
    if request.method == "POST":
        image_url = request.form.get("image_url")

        if image_url:
            try:
                return redirect(url_for("loading_page", image_url=image_url))
            except Exception as err:
                error_message = "Failed to process the image. " + str(err)
                return render_template("landing.html", error_message=error_message)

    return render_template("landing.html", error_message=None)


@app.route("/loading")
def loading_page():
    image_url = request.args.get("image_url")
    return render_template("loading.html", image_url=image_url)


@app.route("/process_image", methods=["POST"])
def process_image_route():
    if request.method == "POST":
        data = request.get_json()
        image_url = data.get("image_url")

        if image_url:
            try:
                # Process the image and generate captions
                summary, sum_response_time, caption_list, cap_response_time = process_image(image_url)

                # Return the captions as a JSON response
                return jsonify({"summary": summary, "sum_response_time": sum_response_time, "caption_list": caption_list, "cap_response_time": cap_response_time})

            except Exception as err:
                error_message = "Error in process_image/\n" + str(err)
                return jsonify({"error": error_message}), 400

    return jsonify({"error": "Error in process_image/\n"}), 400


@app.route("/results")
def results_page():
    image_url = request.args.get("image_url")
    summary = request.args.get("summary")
    sum_response_time = request.args.get("sum_response_time")
    caption_list = request.args.get("caption_list")
    cap_response_time = request.args.get("cap_response_time")

    if image_url and caption_list:
        # Convert the caption list from string to list
        caption_list = json.loads(caption_list)

        return render_template(
            "results.html",
            image_url=image_url,
            summary=summary,
            sum_response_time=sum_response_time,
            caption_list=caption_list,
            cap_response_time=cap_response_time,
        )

    return jsonify({"error": "Invalid request."}), 400


@app.route("/error")
def error_page():
    error_message = request.args.get("error_message")
    print("Error message", error_message)
    return render_template("error.html", error_message=error_message)


def process_image(image_url):
    try:
        response, sum_response_time = imgtotext_api.inference_url(imgtotext_model, image_url)
        print("Sum response time", sum_response_time)
        summary_str = response.text
        summary_dict = json.loads(summary_str)
        summary = summary_dict[0]["generated_text"]

        # Formulate prompt for the caption model
        prompt = captioner_gpt.create_prompt(summary)

        # Request captions from GPT
        caption_list, cap_response_time = captioner_gpt.generate_caption(
            captioner_model, prompt, temp, num_completions
        )
        print("Cap response time", cap_response_time)
        return summary, sum_response_time, caption_list, cap_response_time
    except Exception as err:
        raise Exception("Error in module/\n {}".format(str(err)))


if __name__ == "__main__":
    app.run(debug=True)
    # c = process_image("https://images.unsplash.com/photo-1689758410578-574c8f9eff2b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80")
    # print(c)
