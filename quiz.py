import streamlit as st
import os
import random
from PIL import Image

def quiz():
    data_path = os.path.abspath("./tutor")
    categories = {"Alphabets": "Alphabets", "Numbers": "Numbers", "Phrases": "Phrases", "Words": "Word"}

    st.title("Test Your Knowledge")
    st.write("Take a quiz to test your sign language skills.")

    # Initialize session state for quiz
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0
    if "quiz_answer" not in st.session_state:
        st.session_state.quiz_answer = None
    if "quiz_item" not in st.session_state:
        st.session_state.quiz_item = None
    if "quiz_options" not in st.session_state:
        st.session_state.quiz_options = []
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "quiz_image" not in st.session_state:
        st.session_state.quiz_image = None

    # Generate a new quiz question
    def generate_quiz():
        quiz_category = random.choice(list(categories.keys()))
        quiz_folder = os.path.join(data_path, categories[quiz_category])
        folders = [d for d in os.listdir(quiz_folder) if os.path.isdir(os.path.join(quiz_folder, d))]

        quiz_item = random.choice(folders)
        quiz_path = os.path.join(quiz_folder, quiz_item)
        quiz_images = [img for img in os.listdir(quiz_path) if img.endswith((".jpg", ".jpeg", ".png", ".mp4"))]

        if quiz_images:
            quiz_image = os.path.join(quiz_path, random.choice(quiz_images))
            options = random.sample(folders, min(4, len(folders)))
            if quiz_item not in options:
                options[random.randint(0, len(options) - 1)] = quiz_item

            st.session_state.quiz_item = quiz_item
            st.session_state.quiz_options = options
            st.session_state.quiz_answer = None
            st.session_state.submitted = False
            st.session_state.quiz_image = quiz_image

    # Load or generate quiz question if needed
    if not st.session_state.submitted and not st.session_state.quiz_image:
        generate_quiz()

    # Layout: Image on the left, options on the right
    col1, col2 = st.columns([1, 2])

    with col1:
        if st.session_state.quiz_image:
            if st.session_state.quiz_image.endswith((".jpg", ".jpeg", ".png")):
                st.image(st.session_state.quiz_image, width=150, caption="What does this sign mean?")
            elif st.session_state.quiz_image.endswith(".mp4"):
                st.video(st.session_state.quiz_image)
            else:
                st.error("Unsupported file format.")

    with col2:
        answer = st.radio("Choose the correct answer:", st.session_state.quiz_options, key="quiz_answer", disabled=st.session_state.submitted)

    # Submit button
    if st.button("Submit Answer", disabled=st.session_state.submitted):
        if answer is not None:
            st.session_state.submitted = True
            st.session_state.question_count += 1
            if answer == st.session_state.quiz_item:
                st.session_state.score += 1
                st.success(f"🎉 Correct! This sign means '{st.session_state.quiz_item}'.")
            else:
                st.error(f"❌ Incorrect. The correct answer is '{st.session_state.quiz_item}'.")


    # Display Score
    st.write(f"**Score: {st.session_state.score} / {st.session_state.question_count}**")

    # Next Question Button (Only appears after submission)
    if st.session_state.submitted and st.button("Next Question"):
        st.session_state.submitted = False
        st.session_state.quiz_image = None
        st.rerun()
