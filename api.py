import requests
import os

CLARIFAI_API_KEY = os.getenv("333b0c1305504d25a06847c9d3b59e71")

def identify_food(image_bytes):
    url = "https://api.clarifai.com/v2/models/food-image-recognition/outputs"

    headers = {
        "Authorization": f"Key {CLARIFAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": [
            {
                "data": {
                    "image": {
                        "base64": image_bytes.decode('utf-8')
                    }
                }
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    food_name = data["outputs"][0]["data"]["concepts"][0]["name"]
    confidence = data["outputs"][0]["data"]["concepts"][0]["value"]

    return food_name, confidence
