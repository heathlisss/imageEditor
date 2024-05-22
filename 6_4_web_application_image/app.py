import base64
from flask import Flask, render_template, request, jsonify
import requests
from PIL import Image
from io import BytesIO
from PIL import ImageEnhance

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    if request.method == 'POST':
        url = request.form['url']
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img_data = response.content
                image = Image.open(BytesIO(img_data))
                image_url = url
        except Exception as e:
            print("Error:", e)
    return render_template('index.html', image_url=image_url)


@app.route('/update_image', methods=['POST'])
def update_image():
    try:
        data = request.json
        brightness = float(data.get('brightness', 100)) / 100
        contrast = float(data.get('contrast', 100)) / 100
        sharpness = float(data.get('sharpness', 100)) / 100
        color = float(data.get('color', 100)) / 100

        url = data.get('url')

        response = requests.get(url)
        if response.status_code == 200:
            img_data = response.content
            image = Image.open(BytesIO(img_data))

            enhanced_image = enhance_image(image, brightness, contrast, sharpness, color)

            buffered = BytesIO()
            enhanced_image.save(buffered, format="JPEG")
            processed_image_url = 'data:image/jpeg;base64,' + base64.b64encode(buffered.getvalue()).decode()

            return jsonify({'processed_image_url': processed_image_url})
    except Exception as e:
        print("Error:", e)
    return jsonify({'error': 'Failed to process image'})


def enhance_image(image, brightness, contrast, sharpness, color):
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)

    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness)

    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(color)

    return image


if __name__ == '__main__':
    app.run(debug=True)
