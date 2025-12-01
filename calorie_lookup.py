CALORIE_TABLE = {
    "apple": 95,
    "banana": 105,
    "rice": 206,
    "burger": 354,
    "pizza": 285,
    "egg": 78,
    "bread": 80,
    "chicken": 165,
    "milk": 103,
    "pasta": 131,
}

def get_calories(food):
    food = food.lower()
    return CALORIE_TABLE.get(food, "Unknown")
