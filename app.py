import streamlit as st
import requests
from io import BytesIO

# ---------------------------
# HEIGHT CONVERSION
# ---------------------------
def feet_inches_to_cm(feet, inches):
    return (feet * 12 + inches) * 2.54


# ---------------------------
# BMR / TDEE / MACROS
# ---------------------------
def calculate_bmr(gender, weight, height_cm, age):
    if gender == "Male":
        return 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height_cm - 5 * age - 161

def bmr_feedback(bmr):
    if bmr < 1500:
        return "Your metabolism is a bit slower than average. Focus on lean protein and regular activity."
    elif 1500 <= bmr <= 1800:
        return "Your metabolism is average. Stick to your macros for balanced results."
    else:
        return "Your metabolism is quite fast. You may need slightly higher calories to maintain energy."

def get_activity_multiplier(level):
    levels = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Athlete": 1.9
    }
    return levels[level]


def calculate_tdee(bmr, activity):
    return bmr * get_activity_multiplier(activity)


def calculate_macros(calories, weight, goal):
    if goal == "Bulk":
        protein = 1.8 * weight
    else:
        protein = 2.0 * weight

    protein_cal = protein * 4
    fat_cal = calories * 0.25
    carbs_cal = calories - (protein_cal + fat_cal)

    carbs = carbs_cal / 4
    fat = fat_cal / 9

    return round(protein), round(carbs), round(fat)


# ---------------------------
# FOOD IMAGE CALORIE API (FREE)
# ---------------------------
HF_API_URL = "https://api-inference.huggingface.co/models/nutrify/food-nutrition-estimator"
HF_TOKEN = "YOUR_HF_API_TOKEN"  # <-- replace this


def estimate_food_calories(image_data):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(HF_API_URL, headers=headers, data=image_data)

    try:
        return response.json()
    except:
        return {"error": "Invalid response from API"}


# ============================================
# STREAMLIT UI
# ============================================
st.title("🍎 Fitness Web App — Macros + Calorie Estimator")

st.subheader("1️⃣ Calculate Your TDEE & Macros")

gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", 10, 80)
weight = st.number_input("Weight (kg)", 1.0, 200.0)

col1, col2 = st.columns(2)
with col1:
    feet = st.number_input("Height (feet)", 1, 8)
with col2:
    inches = st.number_input("Height (inches)", 0, 11)

activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Athlete"])

if st.button("Calculate"):
    height_cm = feet_inches_to_cm(feet, inches)
    bmr = calculate_bmr(gender, weight, height_cm, age)
    tdee = calculate_tdee(bmr, activity)

    deficit = tdee - 400
    surplus = tdee + 300

    st.write(f"**BMR:** {bmr:.2f}")
    st.write(f"**TDEE (Maintenance):** {tdee:.2f}")
    st.write(f"**Caloric Deficit:** {deficit:.2f}")
    st.write(f"**Caloric Surplus:** {surplus:.2f}")

    # Macros
    cut_p, cut_c, cut_f = calculate_macros(deficit, weight, "Cut")
    bulk_p, bulk_c, bulk_f = calculate_macros(surplus, weight, "Bulk")

    st.subheader("Macros")
    st.write(f"**Cutting:** {cut_p}g P / {cut_c}g C / {cut_f}g F")
    st.write(f"**Bulking:** {bulk_p}g P / {bulk_c}g C / {bulk_f}g F")

    # ⭐ Feedback based on BMR
    feedback = bmr_feedback(bmr)
    st.subheader("💡 Personalized Feedback")
    st.info(feedback)

# =============================
# FOOD IMAGE CALORIE ESTIMATOR
# =============================
st.subheader("2️⃣ Estimate Calories From Food Image (FREE API)")

uploaded_image = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", width=300)

    if st.button("Estimate Food Calories"):
        image_bytes = uploaded_image.read()

        result = estimate_food_calories(image_bytes)
        st.write("### API Response:")
        st.json(result)
