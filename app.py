### Health Management APP
from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key="AIzaSyBD_N0i-V6pIP0y5zgcHha1pZjSKwbkfX4")

## Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Function to manage chat history
def manage_chat(user_input, response):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    st.session_state.chat_history.append({"user": user_input, "bot": response})

## Initialize our Streamlit app
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
input_prompt = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Analyze Health Condition")

default_input_prompt = """
You are a medical professional. Using the uploaded image and the input description, analyze the overall health condition of the patient. 
Provide a detailed report that includes the following:

1. Identify visible symptoms or conditions.
2. Discuss potential diagnoses based on visual cues.
3. Recommend further medical tests or actions.
4. Suggest general health advice and preventive measures.
5. Mention any urgent signs that require immediate medical attention.

Ensure the analysis is thorough and accurate.
"""

## If submit button is clicked
if submit:
    if uploaded_file is not None:
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, default_input_prompt)
            st.subheader("The Response is")
            st.write(response)
            st.session_state.initial_response = response
            st.session_state.image_data = image_data
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please upload an image to analyze.")

## Chat feature
st.subheader("Chat with the Medical Professional AI")
user_message = st.text_area("Your message:", key="user_message")
send = st.button("Send")

if send and user_message:
    if "image_data" in st.session_state:
        try:
            image_data = st.session_state.image_data
            response = get_gemini_response(user_message, image_data, default_input_prompt)
            manage_chat(user_message, response)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.write("Please analyze the health condition first by uploading an image and clicking the 'Analyze Health Condition' button.")

if "chat_history" in st.session_state:
    st.subheader("Chat History")
    for chat in st.session_state.chat_history:
        st.write(f"You: {chat['user']}")
        st.write(f"AI: {chat['bot']}")
