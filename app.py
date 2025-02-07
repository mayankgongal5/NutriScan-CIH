import os

import openai
import streamlit as st
from openai import OpenAI

from clients import langflow_api_request
from config import OUTPUT_LANGUAGES, LANGFLOW_API_URL, APPLICATION_TOKEN
from utils import extract_text_from_image, analyze_nutrition, text_to_speech

# Set page configuration
st.set_page_config(page_title="NutriScan:Smart Nutrition Label Analyzer", page_icon="🔍", layout="wide")

# App header
st.markdown("<h1>🔍NutriScan: Smart Nutrition Label Analyzer</h1>", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([1, 1.5])

# Section for uploading the food label image
with col1:
    st.markdown("""
        <div class="stCard">
            <h2>📸 Upload Food Label</h2>
            <p>Upload a clear image of any food label to get detailed nutrition analysis.</p>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

    # Output language selector
    output_language = st.selectbox(
        "Select Analysis Language",
        options=list(OUTPUT_LANGUAGES.keys()),
        help="Choose the language for the nutrition analysis output"
    )

if uploaded_file:
    with col1:
        st.image(uploaded_file, caption="Uploaded Label", use_container_width=True)

    try:
        with st.spinner("🔍 Analyzing your food label..."):
            # Extract text using Google Cloud Vision
            image_bytes = uploaded_file.read()
            label_text = extract_text_from_image(image_bytes)

            if label_text:
                # Analyze nutrition with Langflow in the selected language
                nutrition_analysis = analyze_nutrition(label_text, output_language.split()[0])

                with col2:
                    st.markdown("""
                        <div class="stCard">
                            <h2>🍎 Nutrition Analysis</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(nutrition_analysis)

                    # Convert text to speech
                    audio_bytes = text_to_speech(nutrition_analysis)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")
            else:
                st.warning("⚠️ No text found in the image. Please upload a clearer image.")

    except Exception as e:
        st.error(f"❌ Error processing image: {e}")

# Chat feature - Ask AI (Langflow) questions based on the output
# with st.expander("💬 Chat with AI"):
#     # Create a session state to store conversation history
#     if 'messages' not in st.session_state:
#         st.session_state.messages = []
#
#     # Display chat history
#     for message in st.session_state.messages:
#         st.markdown(f"**{message['role']}**: {message['content']}")
#
#     # User input
#     user_message = st.text_input("Ask a question:", "")
#
#     if user_message:
#         # Append user message to conversation history
#         st.session_state.messages.append({"role": "user", "content": user_message})
#
#         # Send query to Langflow API and get the response
#         response = langflow_api_request(user_message)
#
#         # Append Langflow's response to conversation history
#         st.session_state.messages.append({"role": "AI", "content": response})
#
#         # Display the response
#         st.markdown(f"**AI**: {response}")

with st.expander("💬 Chat with AI"):
    # Initialize session state for messages and Langflow response
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'langflow_response' not in st.session_state:
        st.session_state.langflow_response = ""

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_message = st.chat_input("Ask a question:")

    if user_message:
        # Append user message to conversation history
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Prepare the context for OpenAI
        context = []
        if st.session_state.langflow_response:
            context.append({"role": "system", "content": f"Langflow response: {st.session_state.langflow_response}"})
        context.append({"role": "user", "content": user_message})

        # Call OpenAI API
        try:
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            response = client.chat.completions.create(
                model="gpt-4",  # Ensure you're using the correct model
                messages=context,
                max_tokens=150,
                temperature=0.7
            )

            # Extract the AI's response
            ai_response = response.choices[0].message.content.strip()

            # Append AI's response to conversation history
            st.session_state.messages.append({"role": "AI", "content": ai_response})

            # Display the response
            with st.chat_message("AI"):
                st.markdown(ai_response)

        except Exception as e:
            st.error(f"❌ Error calling OpenAI API: {e}")


# Information section at the bottom
with st.expander("ℹ️ About this App"):
    st.markdown("""
        <div padding: 1rem; border-radius: 0.5rem;'>
            <h3 style='color: #1E88E5;'>How it works</h3>
            <p>This smart analyzer uses advanced AI to help you understand food labels better:</p>
            <ol>
                <li>Google Cloud Vision extracts text from your food label image</li>
                <li>Langflow analyzes the nutritional content</li>
                <li>Get instant insights about calories, nutrients, and health recommendations</li>
                <li>Ask questions about the analysis and chat with AI</li>
            </ol>
            <p><em>Note: This is a demonstration tool. Always consult with healthcare professionals for dietary advice.</em></p>
        </div>
    """, unsafe_allow_html=True)
