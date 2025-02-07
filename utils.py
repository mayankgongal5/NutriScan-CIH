import os

from google.cloud import vision
from clients import vision_client
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
# Extract text from image using Google Cloud Vision
try:
    openai.api_key = openai_api_key
    openai_client = openai.Client(api_key=openai_api_key)
except Exception as e:
    raise Exception(f"Error initializing OpenAI client: {e}")
def analyze_nutrition(text, language):
    try:
        system_prompt = f"""You are a nutrition expert analyzing food labels. 
        Provide responses in {language}. 
        Focus on:
        1. Calories and serving size
        2. Macronutrients (protein, carbs, fats)
        3. Important vitamins and minerals
        4. Allergens and warnings
        5. Health insights and recommendations
        and give your opinion if the food is good for you or not 

        Format the output using Markdown for better readability.
        Use emojis appropriately to make the output more engaging."""

        user_prompt = f"""Analyze this food label text and provide a detailed nutritional analysis:

        {text}"""

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"OpenAI API Error: {e}")
def text_to_speech(text):
    try:
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice="coral",
            input=text  # No need for 'language' here
        )
        return response.content
    except Exception as e:
        raise Exception(f"Error converting text to speech: {e}")
def extract_text_from_image(image_bytes):
    try:
        image = vision.Image(content=image_bytes)
        response = vision_client.text_detection(image=image)

        if response.error.message:
            raise Exception(f"Google Cloud Vision API Error: {response.error.message}")

        texts = response.text_annotations
        return texts[0].description if texts else ""
    except Exception as e:
        raise Exception(f"Error processing image: {e}")
