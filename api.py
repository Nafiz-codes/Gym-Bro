import requests
import base64
import os

CLARIFAI_API_KEY = os.getenv("333b0c1305504d25a06847c9d3b59e71")

def identify_food(image_bytes):
    url = "https://api.clarifai.com/v2/models/food-item-recognition/outputs"

    headers = {
        "Authorization": f"Key {CLARIFAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # ✅ Correct: convert bytes → base64 string
    b64_image = base64.b64encode(image_bytes).decode('utf-8')

    payload = {
        "inputs": [
            {
                "data": {
                    "image": {
                        "base64": b64_image
                    }
                }
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    # Grab highest-confidence food prediction
    concepts = data["outputs"][0]["data"]["concepts"]
    if not concepts:
        return None, None

    food_name = concepts[0]["name"]
    confidence = concepts[0]["value"]

    return food_name, confidence

