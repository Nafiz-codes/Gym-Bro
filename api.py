import os
import base64
import requests

# Your Personal Access Token from Clarifai
CLARIFAI_PAT = os.getenv("333b0c1305504d25a06847c9d3b59e71")  # Make sure to set this in Streamlit Cloud or .env

# Clarifai shared model info
USER_ID = "clarifai"
APP_ID = "main"
MODEL_ID = "food-item-recognition"

def identify_food(image_bytes):
    """
    Takes raw image bytes, sends to Clarifai food-item-recognition model,
    and returns the most probable food name and confidence.
    """
    if CLARIFAI_PAT is None:
        print("Error: CLARIFAI_PAT not set.")
        return None, None

    url = f"https://api.clarifai.com/v2/users/clarifai/apps/main/models/food-item-recognition/outputs"

    headers = {
        "Authorization": f"Key {CLARIFAI_PAT}",
        "Content-Type": "application/json"
    }

    # Base64 encode the image bytes
    b64_image = base64.b64encode(image_bytes).decode('utf-8')

    payload = {
        "inputs": [
            {
                "data": {
                    "image": {"base64": b64_image}
                }
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
    except Exception as e:
        print(f"Clarifai API request failed: {e}")
        return None, None

    # Safe extraction of concepts
    outputs = data.get("outputs", [])
    if not outputs:
        return None, None

    concepts = outputs[0].get("data", {}).get("concepts", [])
    if not concepts:
        return None, None

    # Return highest-confidence concept
    food_name = concepts[0].get("name", None)
    confidence = concepts[0].get("value", None)

    return food_name, confidence
