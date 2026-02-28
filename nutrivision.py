import streamlit as st
from PIL import Image
from ai_engine import analyze_food_image, configure_genai

# Page Config
st.set_page_config(page_title="NutriVision AI", page_icon="🥗", layout="wide")

# Sidebar
st.sidebar.title("🥗 NutriVision")
st.sidebar.info("Upload a food image to get an instant nutritional analysis.")

# Main app
st.title("NutriVision: AI Food Analyzer 🍎")
st.markdown("### Discover what's on your plate with the power of Gemini AI.")

# API Check
status, msg = configure_genai()
if not status:
    st.error("⚠️ API Key Error")
    st.warning(msg)
    st.stop()

# Image Upload
uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width="stretch")
    
    with col2:
        st.subheader("Analysis")
        if st.button("🔍 Analyze Nutrition"):
            with st.spinner("Analyzing image... Please wait..."):
                result = analyze_food_image(image)
                st.markdown(result)
                st.success("Analysis Complete!")

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini 1.5 Flash")
