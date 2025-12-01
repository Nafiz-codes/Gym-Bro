from api import identify_food

# Replace with a clear image of a food item
image_path = "crispy-mixed-pizza-with-olives-sausage.jpg"  

with open(image_path, "rb") as f:
    image_bytes = f.read()

food, confidence = identify_food(image_bytes)
print("Detected food:", food)
print("Confidence:", confidence)
