from flask import Flask, render_template, request
import requests
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

CRUNCHY_PLATYPUS = "AIzaSyBd2jJqqkUnYlAbPailiDno8ngMomLVQEE"
SPARKLY_TACO_DIMENSION = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    # Convert RGBA/LA/P images to RGB
    if image.mode in ('RGBA', 'LA', 'P'):
        rgb_image = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'RGBA':
            rgb_image.paste(image, mask=image.split()[-1])
        else:
            rgb_image.paste(image)
        image = rgb_image
    image.save(buffered, format="JPEG", quality=90)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

@app.route("/", methods=["GET", "POST"])
def index():
    output_text = None
    if request.method == "POST":
        if "image" in request.files:
            image_file = request.files["image"]
            if image_file:
                try:
                    # Read and process image
                    image_bytes = image_file.read()
                    image = Image.open(BytesIO(image_bytes))
                    
                    # Resize large images for faster processing
                    image.thumbnail([1024, 1024], Image.Resampling.LANCZOS)
                    
                    # Convert to base64
                    base64_image = encode_image_to_base64(image)
                    
                    # Build the Gemini API request payload
                    prompt_text = (
                        "Analyze this food image and provide:\n"
                        "1) Food name and category\n"
                        "2) Estimated nutrients per serving (carbs, protein, fat in grams)\n"
                        "3) Estimated calories\n"
                        "4) Sustainability score out of 100 with brief explanation\n"
                        "5) Additional health notes"
                    )
                    
                    payload = {
                        "contents": [
                            {
                                "parts": [
                                    {
                                        "text": prompt_text
                                    },
                                    {
                                        "inline_data": {
                                            "mime_type": "image/jpeg",
                                            "data": base64_image
                                        }
                                    }
                                ]
                            }
                        ],
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 2048
                        }
                    }
                    
                    # Make request to Gemini API
                    print("Sending request to Gemini Vision API...")
                    response = requests.post(
                        f"{SPARKLY_TACO_DIMENSION}?key={CRUNCHY_PLATYPUS}",
                        json=payload,
                        timeout=60
                    )
                    
                    # Handle errors
                    if not response.ok:
                        error_data = response.json() if response.text else {}
                        error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                        print(f"API Error: {error_data}")
                        raise Exception(f"Gemini API error: {error_msg}")
                    
                    data = response.json()
                    
                    # Extract the response text
                    if 'candidates' in data and len(data['candidates']) > 0:
                        candidate = data['candidates'][0]
                        if 'content' in candidate and 'parts' in candidate['content']:
                            parts = candidate['content']['parts']
                            if len(parts) > 0 and 'text' in parts[0]:
                                output_text = parts[0]['text'].replace('\n', '<br>')
                            else:
                                output_text = "No text response from API"
                        else:
                            output_text = "Invalid response structure from API"
                    else:
                        output_text = "No response from API"
                    
                except requests.exceptions.Timeout:
                    output_text = "Request timed out. The image might be too large. Try a smaller image."
                except requests.exceptions.RequestException as e:
                    output_text = f"Network error: {str(e)}"
                except Exception as e:
                    output_text = f"Error: {str(e)}"
                    print(f"Full error details: {e}")
        else:
            output_text = "Please upload an image."
    
    return render_template("index.html", output_text=output_text)

if __name__ == "__main__":
    app.run(debug=True, port=5000)