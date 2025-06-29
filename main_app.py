# maize_fertility_app.py

import streamlit as st
import numpy as np
import joblib

# Load trained model
model = joblib.load('model_rdf.pkl')  # Ensure model_rdf.pkl is in the same directory

# Fertilizer recommendation logic
def recommend_fertilizer(N, P, K):
    recommendation = []
    if N < 80:
        recommendation.append("Apply Nitrogen-rich fertilizer (e.g., Urea)")
    if P < 30:
        recommendation.append("Apply Phosphorus-rich fertilizer (e.g., SSP)")
    if K < 40:
        recommendation.append("Apply Potassium-rich fertilizer (e.g., MOP)")
    if not recommendation:
        return "Soil nutrient levels are adequate. Use balanced fertilizer."
    return ", ".join(recommendation)

# Optimized fertilizer application (stage-based)
def fertilizer_schedule(N, P, K):
    return {
        "Pre-Planting": recommend_fertilizer(N, P, K),
        "Mid-Growth": "Use foliar feed or compost to sustain growth.",
        "Post-Harvest": "Apply organic manure to restore soil." 
    }

# App layout setup
st.set_page_config(page_title="🌽 Maize Suitability App", layout="centered")

# Sidebar - About Section
st.sidebar.title("ℹ️ About This App")
st.sidebar.markdown("""
### 🌽 Decision Support System for Maize Crop

This intelligent tool assists farmers, students, and researchers in:

- ✅ Evaluating **soil fertility** (N, P, K, pH)
- ✅ Determining **maize suitability** based on weather and soil conditions
- ✅ Recommending **fertilizer type and dosage**
- ✅ Suggesting a stage-based **fertilizer application plan**
""")
---

### ⚙️ How it Works

- A **trained machine learning model** (Random Forest) classifies the soil as **suitable or not** for maize.
- Nutrient levels are analyzed to generate **custom fertilizer recommendations**.
- It also suggests a **3-stage plan** to optimize yield and reduce environmental impact.

---

# Main App Title and Form
st.title("🌾 Maize Soil Fertility & Fertilizer Advisor")
st.markdown("Input your soil and weather data below to get insights.")

with st.form("input_form"):
    N = st.number_input("Nitrogen (N)", min_value=0.0)
    P = st.number_input("Phosphorus (P)", min_value=0.0)
    K = st.number_input("Potassium (K)", min_value=0.0)
    temp = st.number_input("Temperature (°C)", min_value=0.0)
    humidity = st.number_input("Humidity (%)", min_value=0.0)
    ph = st.number_input("Soil pH", min_value=0.0)
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0)
    submit = st.form_submit_button("Analyze")

if submit:
    # Input validation
    if any(val == 0.0 for val in [N, P, K, temp, humidity, ph, rainfall]):
        st.error("🚫 Please fill in all the required values. None should be left at zero.")
    else:
        user_input = np.array([[N, P, K, temp, humidity, ph, rainfall]])
        pred = model.predict(user_input)[0]

        st.subheader("🔍 Soil Suitability for Maize:")
        if pred == 1:
            st.success("✅ This soil is suitable for maize cultivation.")
        else:
            st.warning("⚠️ This soil is not ideal for maize. Consider improvements.")

        st.subheader("🌱 Fertilizer Recommendation:")
        st.write(recommend_fertilizer(N, P, K))

        st.subheader("📅 Optimized Fertilizer Schedule:")
        schedule = fertilizer_schedule(N, P, K)
        for stage, advice in schedule.items():
            st.markdown(f"**{stage}:** {advice}")

        st.subheader("🌽 Crop Suitability Based on pH and Rainfall:")
        if 5.5 <= ph <= 7.5 and 20 <= rainfall <= 200:
            st.info("✅ Maize is suitable under these pH and rainfall conditions.")
        else:
            st.error("❌ Conditions may not favor maize. Consider soil amendment or other crops.")
