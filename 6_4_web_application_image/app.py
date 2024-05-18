import base64

from flask import Flask, render_template, request
import requests
from PIL import Image
from io import BytesIO
from PIL import ImageEnhance

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    image = None
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


@app.route('/', methods=['POST'])
def update_image():
    try:
        # Получение данных из запроса
        brightness = float(request.json.get('brightness', 0))/50
        contrast = float(request.json.get('contrast', 0))/50
        url = request.json.get('url')

        # Получение изображения по URL
        response = requests.get(url)
        if response.status_code == 200:
            img_data = response.content
            image = Image.open(BytesIO(img_data))

            # Обновление яркости и контрастности
            enhanced_image = enhance_image(image, brightness, contrast)

            # Преобразование изображения в base64
            buffered = BytesIO()
            enhanced_image.save(buffered, format="JPEG")
            processed_image_url = 'data:image/jpeg;base64,' + base64.b64encode(buffered.getvalue()).decode()

            # Возврат обработанного изображения
            return {'processed_image_url': processed_image_url}
    except Exception as e:
        print("Error:", e)
    return {'error': 'Failed to process image'}


def enhance_image(image, brightness, contrast):
    # Обработка изображения с учетом переданных значений яркости и контрастности
    brightness_factor = brightness
    contrast_factor = contrast
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)

    return image


if __name__ == '__main__':
    app.run(debug=True)
