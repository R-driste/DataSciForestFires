import sys
import json
import base64
import tempfile
import torch
from torchvision import models, transforms
import torch.nn as nn
from PIL import Image
from playsound import playsound

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

model = models.resnet18()
model.fc = nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load("heavy_zip/vision/resnet18_amalgam.pth", map_location=device))
model = model.to(device)
model.eval()

class_names = ['fire', 'nofire']

def predict_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(image)
        pred = torch.argmax(output, dim=1).item()
    return class_names[pred]

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
explanation = f"This {image_type.lower()} image was classified as {prediction.lower()}."

print(json.dumps({
    "prediction": prediction,
    "explanation": explanation
}))

playsound('tada-fanfare-a-6313.mp3')