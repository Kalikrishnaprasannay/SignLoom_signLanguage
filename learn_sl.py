import streamlit as st
import os
from PIL import Image

def learn_sl():
    data_path = "./tutor"
    categories = {"Alphabets": "Alphabets", "Numbers": "Numbers", "Phrases": "Phrases", "Words": "Word"}  # Match actual folder name

    st.title("Learn Sign Language")
    st.write("Learn basic sign language through images.")

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    category = st.selectbox("Select a category:", list(categories.keys()), key="category_select")

    if category != st.session_state.selected_category:
        st.session_state.selected_category = category
        st.session_state.user_input = ""

    category_path = os.path.join(data_path, categories[category])
    if not os.path.exists(category_path):
        st.error(f"Error: Category path '{category_path}' does not exist.")
        return

    folders = [d for d in os.listdir(category_path) if os.path.isdir(os.path.join(category_path, d))]

    if category in ["Alphabets", "Numbers"]:
        user_input = st.text_input("Enter a letter or number:", value=st.session_state.user_input, key="user_input").strip()
        if user_input:
            input_path = os.path.join(category_path, user_input.upper())
            if os.path.exists(input_path):
                images = [img for img in os.listdir(input_path) if img.lower().endswith((".jpg", ".jpeg", ".png"))]
                if images:
                    cols = st.columns(3)
                    for i, img in enumerate(images[:3]):
                        image = Image.open(os.path.join(input_path, img))
                        cols[i % 3].image(image, caption=user_input.upper(), use_container_width=True)
                else:
                    st.write("No images found for this input.")
            else:
                st.write("No directory found for this input.")

    elif category == "Phrases":
        phrase = st.selectbox("Choose a phrase:", folders)
        phrase_path = os.path.join(category_path, phrase)
        if os.path.exists(phrase_path):
            images = [img for img in os.listdir(phrase_path) if img.lower().endswith((".jpg", ".jpeg", ".png"))]
            if images:
                cols = st.columns(3)
                for i, img in enumerate(images[:3]):
                    image = Image.open(os.path.join(phrase_path, img))
                    cols[i % 3].image(image, caption=phrase, use_container_width=True)
            else:
                st.write("No images found for this phrase.")
        else:
            st.write("No directory found for this phrase.")

    elif category == "Words":
        user_input = st.text_input("Enter a word:", value=st.session_state.user_input, key="word_input").strip()
        if user_input:
            input_path = os.path.join(category_path, user_input.capitalize())  # Ensure correct casing
            if os.path.exists(input_path):
                images = [img for img in os.listdir(input_path) if img.lower().endswith((".jpg", ".jpeg", ".png"))]
                if images:
                    cols = st.columns(3)
                    for i, img in enumerate(images[:3]):
                        image = Image.open(os.path.join(input_path, img))
                        cols[i % 3].image(image, caption=user_input.capitalize(), use_container_width=True)
                else:
                    st.write("No images found for this word.")
            else:
                st.write("No directory found for this word.")
