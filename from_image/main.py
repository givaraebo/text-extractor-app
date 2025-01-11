import os
import cv2
import numpy as np
import pytesseract
import requests

from config.config import config

class TextExtractor:

    def __init__(self):
        pass

    def from_captcha_image(self, image_path):
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, threshold_image = cv2.threshold(gray_image, 145, 255, cv2.THRESH_BINARY)
        blurred_image = cv2.medianBlur(threshold_image, 3)
        text = pytesseract.image_to_string(blurred_image)
        return text

    def from_captcha_image_url(self, image_url):
        # Lade das Bild von der URL
        response = requests.get(image_url)

        # Konvertiere das Bild in ein NumPy-Array
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        # Lade das Bild in OpenCV
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, threshold_image = cv2.threshold(gray_image, 160, 255, cv2.THRESH_BINARY)
        blurred_image = cv2.medianBlur(threshold_image, 3)
        text = pytesseract.image_to_string(blurred_image)
        return text



image_path = os.path.join(config.images_dir, 'examples/captcha.png')
image_url = 'https://images-na.ssl-images-amazon.com/captcha/sgkknrsj/Captcha_kwszdrrwqg.jpg'

text_extractor = TextExtractor()
text1 = text_extractor.from_captcha_image(image_path)
text2 = text_extractor.from_captcha_image_url(image_url)

print(text1)
print(text2)