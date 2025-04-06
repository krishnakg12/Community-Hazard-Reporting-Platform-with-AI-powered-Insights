import base64
import requests

image_path = "C:\\Users\\krish\\Downloads\\flood.jpeg"

# Convert image to Base64
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# API Request
url = "http://127.0.0.1:5000/api/predict"
data = {
    "description": "Flooding has occurred due to heavy rains.",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "image_base64": encoded_image
}

  