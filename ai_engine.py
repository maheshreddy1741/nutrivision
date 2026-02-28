import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def configure_genai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return False, "Google API Key not found. Please set it in the .env file."
    genai.configure(api_key=api_key)
    return True, "Success"

def analyze_food_image(image, custom_prompt=None):
    """
    Analyzes an image using Google Gemini Pro Vision.
    """
    # model = genai.GenerativeModel('gemini-pro-vision') # Deprecated or might change, using generic acceptable name if possible or latest
    # Update: 'gemini-1.5-flash' is often recommended for multi-modal speed/cost, checking if 'gemini-pro-vision' is still valid standard. 
    # Let's use 'gemini-1.5-flash' for better performance if available, or fallback to 'gemini-pro-vision'.
    # For safety in this prompt, I will use 'gemini-1.5-flash' as it is the current standard for multimodal.
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        base_prompt = """
        Analyze this food image and provide a detailed nutritional breakdown. 
        Format the response as follows:
        
        ## 🍽️ Food Identification
        Identify the main dish and ingredients.

        ## 📊 Nutritional Estimate (Approximate)
        | Item | Calories | Protein (g) | Carbs (g) | Fat (g) |
        |---|---|---|---|---|
        | Total | ... | ... | ... | ... |
        
        ## 🥗 Health Rating (1-10)
        Give a score and a brief explanation.

        ## 💡 Observations
        Any dietary notes (e.g., "High in sugar", "Good source of fiber", "Gluten-free?").
        """
        
        prompt = custom_prompt if custom_prompt else base_prompt
        
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

if __name__ == "__main__":
    status, msg = configure_genai()
    print(msg)
