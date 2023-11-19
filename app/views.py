# Important imports
from app import app
from flask import request, render_template, url_for
import os
import numpy as np
from PIL import Image
from vision import GPT_Vision



app.config.from_object('config.DevelopmentConfig') 

@app.route("/", methods=["GET", "POST"])
def index():
    # Execute if request is get
    if request.method == "GET":
        full_filename = 'images/white_bg.jpg'
        return render_template("index.html", full_filename=full_filename)

    # Execute if request is post
    if request.method == "POST":
        image_upload = request.files['image_upload']
        imagename = image_upload.filename

        # Ensure the 'uploads' directory exists
        uploads_dir = app.config['UPLOADS']
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        # Save the image to the 'uploads' directory
        image_path = os.path.join(uploads_dir, imagename)
        image_upload.save(image_path)

        GPT = GPT_Vision(image_path)

        print("Uploaded Image:", imagename)
        print("Image saved to static folder:", image_path)

        # Returning template, filename, extracted text
        return render_template('index.html', full_filename=imagename, image=image_path, gpt_response=GPT)

# Main function
if __name__ == '__main__':
    app.run(debug=True)
