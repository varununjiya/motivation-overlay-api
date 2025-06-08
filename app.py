from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import uuid

app = Flask(__name__)

@app.route('/overlay', methods=['POST'])
def overlay():
    data = request.json
    image_url = data.get("image_url")
    quote = data.get("quote", "")

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    image.thumbnail((1080, 1080))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("OpenSans-Regular.ttf", 40)

    def wrap(text, width):
        lines = []
        while text:
            if len(text) <= width: break
            split = text[:width].rfind(" ")
            lines.append(text[:split] if split != -1 else text[:width])
            text = text[split:].lstrip()
        lines.append(text)
        return "\n".join(lines)

    wrapped = wrap(quote, 40)
    W, H = image.size
    w, h = draw.multiline_textsize(wrapped, font=font)
    draw.multiline_text(((W-w)/2, H-h-30), wrapped, font=font, fill="white", align="center")

    filename = f"/tmp/{uuid.uuid4()}.jpg"
    image.save(filename, format="JPEG")
    return send_file(filename, mimetype="image/jpeg")

@app.route('/')
def index():
    return "Overlay API is running!"
