from flask import Flask, render_template, request, url_for
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)

TOMATO = "AIzaSyB9_ALEj1KbhQU84rTqtErcwJPauDNKriE"
genai.configure(api_key=TOMATO)
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route("/", methods=["GET", "POST"])
def index():
    output_text = None
    if request.method == "POST":
        if "image" in request.files:
            image_file = request.files["image"]
            if image_file:
                try:
                    image_bytes = image_file.read()
                    image = Image.open(BytesIO(image_bytes))
                    image.thumbnail([1024, 1024], Image.Resampling.LANCZOS)
                    prompt = request.form.get("prompt", "Analyze the given food image in detail. Provide the following information in a structured format:1. Food Name: (Identify the food item) 2.Food Category: (e.g., Snack, Dessert, Main Course, Fruit, Vegetable) 3.  Nutrient Breakdown (per serving): Macronutrients:   Carbohydrates: (grams) Sugars: (grams) Fat: (grams) Protein: (grams) Micronutrients: (List key vitamins and minerals, if detectable) 4.  Calorie Count (per serving): (calories) 5.Sustainability Score (out of 100): (score) 6.Sustainability Explanation: (Explain the reasoning behind the sustainability score, considering factors like ingredients, processing, and packaging) 7. Additional Notes:** (Any other relevant information about the food) Provide estimates where exact values are not possible, and indicate that they are estimates.")
                    response = model.generate_content([prompt, image])
                    output_text = response.text.replace('\n', '<br>') # Keep line breaks
                except Exception as e:
                    output_text = f"An error occurred: {e}"
        else:
            output_text = "Please upload an image."
    return render_template("index.html", output_text=output_text)

if __name__ == "__main__":
    app.run(debug=True)