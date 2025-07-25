'''
This python helper script is used to classify the input satellite image for fire.
'''
import sys
import json
import base64
import tempfile
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import ImageFile, Image
import simpleaudio as sa
import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

wave_obj = sa.WaveObject.from_wave_file(os.path.join(BASE_DIR, 'audio', 'clock.wav'))
play_obj = wave_obj.play()
play_obj.wait_done()

#avoid interrupting the json for later use
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.ERROR)

ImageFile.LOAD_TRUNCATED_IMAGES = True

#load model from weights
model = load_model(os.path.join(BASE_DIR, 'heavy_zip', 'vision', 'secondmod.h5'))
class_names = ['nofire', 'fire']

def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def predict_image(image_path):
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array, verbose=0)[0][0]
    return class_names[int(prediction > 0.5)]

form_data = json.load(sys.stdin)
base64_data = form_data["base64"]
image_type = form_data.get("imageType", "Unknown")

if "," in base64_data:
    base64_data = base64_data.split(",")[1]

image_bytes = base64.b64decode(base64_data)
with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
    tmp.write(image_bytes)
    tmp_path = tmp.name

prediction = predict_image(tmp_path)
explanation = f"This {image_type.lower()} image was classified as {prediction.lower()} :D"

wave_obj = sa.WaveObject.from_wave_file(os.path.join(BASE_DIR, 'audio', 'positive.wav'))
play_obj = wave_obj.play()
play_obj.wait_done()

print(json.dumps({
    "prediction": prediction,
    "explanation": explanation
}))