import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
from PIL import Image
import os
import pyttsx3
import threading
import time
from difflib import SequenceMatcher
def sentences():
    # Load the trained model with error handling if not already loaded
    if "model" not in st.session_state:
        try:
            model_path = "./sign_language_Sentence_model.keras"
            if os.path.exists(model_path):
                st.session_state["model"] = tf.keras.models.load_model(model_path)
                st.success("Model loaded successfully!")
            else:
                st.error(f"Model file not found: {model_path}")
        except Exception as e:
            st.error(f"Error loading model: {e}")
            st.session_state["model"] = None

    # Load class indices (auto-detect from dataset folders)
    if "index_to_class" not in st.session_state:
        class_indices = {}
        index_to_class = {}
        try:
            folders = sorted(os.listdir("./tutor/Word"))
            if folders:
                class_indices = {v: k for k, v in enumerate(folders)}
                index_to_class = {v: k for k, v in class_indices.items()}
                st.session_state["index_to_class"] = index_to_class
                st.success("Class mappings loaded successfully!")
            else:
                st.error("No sign class folders found in Pages/Frame")
        except Exception as e:
            st.error(f"Error loading class indices: {e}")
            st.session_state["index_to_class"] = {}

    # Initialize MediaPipe Hand Detection
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    # Initialize Text-to-Speech with error handling
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 150)  # Adjust speed
    tts_engine.setProperty('volume', 1.0)  # Max volume

    def speak_text(text):
        try:
            thread = threading.Thread(target=lambda: tts_engine.say(text) or tts_engine.runAndWait())
            thread.start()
        except Exception as e:
            st.error(f"Speech synthesis error: {e}")

    # Dictionary to map sign language sentences to English sentences
    sign_to_english = {
        "i love you": "I Love You","you friend my": "You are my friend",
        "He play like": "He likes to play","she want book": "She wants a book",
        "we go house now": "We go home now","they meet school": "They meet at school",
        "my phone big" : "My phone is big","me have money" : "I have money",
        "please help me" : "Please, Help me","you name what" : "What is your name?",
        "my car where" : "Where is my car?","food me like" : "I like the food",
        "why you stop" : "Why did you stop","how help me" : "How can I help?",
        "this book my" : "This is my book","that wrong" : "That is wrong",
        "now night" : "It is night now","time sleep" : "Time to sleep",
        "me happy now" : "I am happy now","now what time" : "What is the time now?",
        "no this bad" : "No, this is bad","me want food now" : "I want food now",
        "go school please" : "Please, go to school","have food please" : "Please, have the food",
        "you where" : "Where are you?","we want money" : "We need money",
        "me know you" : "I know you","they want food" : "They want food",
        "she happy" : "She is happy","it good" : "It is good",
        "Me want food now" : "I want food now","we meet school" : "We meet at school",
        "they friend my" : "They are my friends","she go house now" : "She goes home now",
        "you have phone my" : "You have my phone","they play school" : "They play at school",
        "me want sleep" : "I want to sleep","we have food now" : "We have food now",
        "we learn signlanguage" : "We learn Sign Language","My House small" : "My home is small",
    }

    # Function to find the best matching sentence with fallback
    def map_to_english(sentence):
        sentence = sentence.lower()
        best_match = None
        best_similarity = 0

        for key, value in sign_to_english.items():
            similarity = SequenceMatcher(None, sentence, key).ratio()
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = value
            if similarity >= 0.7:
                return value

        return best_match if best_match else "No suitable match found"

    # Preprocess Frame Function
    def preprocess_frame(frame):
        tensor = tf.image.resize(frame, [128, 128])
        tensor = tf.cast(tensor, tf.float32) / 255.0  # Normalize
        tensor = tf.expand_dims(tensor, axis=0)  # Add batch dimension
        return tensor

    # Function to Predict Sign with a buffer for 2 seconds
    word_buffer = {}
    constructed_sentence = []
    def predict_sign(frame):
        model = st.session_state.get("model", None)
        index_to_class = st.session_state.get("index_to_class", {})

        if model is None:
            return "Error: Model not loaded", 0.0
        if not index_to_class:
            return "Error: Class mappings not loaded", 0.0

        processed_frame = preprocess_frame(frame)
        try:
            predictions = model.predict(processed_frame)
            pred_index = np.argmax(predictions[0])
            pred_class = index_to_class.get(pred_index, "Unknown")
            confidence = np.max(predictions[0]) * 100

            current_time = time.time()
            if pred_class in word_buffer:
                word_buffer[pred_class]['count'] += 1
                if current_time - word_buffer[pred_class]['start_time'] >= 2:
                    if pred_class not in constructed_sentence:
                        constructed_sentence.append(pred_class)
                    return pred_class, confidence
            else:
                word_buffer[pred_class] = {'start_time': current_time, 'count': 1}

            return "", 0.0
        except Exception as e:
            return f"Prediction error: {e}", 0.0



    # ---- STREAMLIT UI ----
    st.title("SignLoom: Sentences")

    # Initialize session state variables
    if "recording" not in st.session_state:
        st.session_state["recording"] = False

    if "sentence" not in st.session_state:
        st.session_state["sentence"] = []
    final_sentence=""
    mapped_sentence=""

    # Option to use Webcam or Upload Video
    option = st.radio("Choose input method:", ("Use Webcam", "Upload Video"))

    # Buttons for recording
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Recording"):
            if st.session_state.get("model") is None:
                st.error("Model not loaded. Cannot start recording.")
            else:
                st.session_state["recording"] = True
                st.session_state["sentence"] = []  # Reset sentence

    with col2:
        if st.button("Stop Recording"):
            st.session_state["recording"] = False
            if st.session_state["sentence"]:
                final_sentence = " ".join(dict.fromkeys(st.session_state["sentence"]))  # Remove duplicates
                mapped_sentence = map_to_english(final_sentence)
            else:
                final_sentence = "No signs detected."
                mapped_sentence = ""

    st.text_area("Constructed Sentence:", final_sentence)
    st.text_area("Mapped English Sentence:", mapped_sentence)

    if mapped_sentence and mapped_sentence != "Could not map to a known sentence.":
        speak_text(mapped_sentence)  # Speak mapped sentence

    # Placeholder for displaying detected sign
    detected_sign_placeholder = st.empty()

    if option == "Use Webcam":
        st.write("Real-time Sign Language Recognition")

        # Open Webcam
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7) as hands:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(rgb_frame)

                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Predict Sign
                    pred_class, confidence = predict_sign(rgb_frame)
                    cleaned_pred_class = pred_class.replace("_", " ")

                    if st.session_state["recording"]:
                        if cleaned_pred_class and cleaned_pred_class != "Unknown":
                            if not st.session_state["sentence"] or st.session_state["sentence"][-1] != cleaned_pred_class:
                                st.session_state["sentence"].append(cleaned_pred_class)

                    # Display current detected word
                    detected_sign_placeholder.text(f"Detected Sign: {cleaned_pred_class}")

                # Display Frame in Streamlit
                stframe.image(frame, channels="BGR")


        cap.release()
        cv2.destroyAllWindows()
    if option == "Upload Video":
        uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
        if uploaded_file:
            temp_video_path = "temp_video.mp4"
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.read())
            cap = cv2.VideoCapture(temp_video_path)
            constructed_sentence = []
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pred_class, _ = predict_sign(rgb_frame)
                if pred_class and pred_class != "Unknown":
                    constructed_sentence.append(pred_class)
            cap.release()
            os.remove(temp_video_path)
            final_sentence = " ".join(dict.fromkeys(constructed_sentence))
            mapped_sentence = map_to_english(final_sentence)
            st.text_area("Constructed Sentence:", final_sentence)
            st.text_area("Mapped English Sentence:", mapped_sentence)
            if mapped_sentence:
                speak_text(mapped_sentence)
