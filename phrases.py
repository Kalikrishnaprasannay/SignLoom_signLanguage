import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
from PIL import Image
import os
import pyttsx3
import threading

def phrases():
    # Load the trained model with error handling
    try:
        model = tf.keras.models.load_model("./sign_language_model_transfer.keras")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        model = None

    # Load class indices (auto-detect from dataset folders)
    class_indices = {v: k for k, v in enumerate(sorted(os.listdir("./tutor/Phrases")))}
    index_to_class = {v: k for k, v in class_indices.items()}

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

    # Preprocess Frame Function
    def preprocess_frame(frame):
        tensor = tf.image.resize(frame, [128, 128])
        tensor = tf.cast(tensor, tf.float32) / 255.0  # Normalize
        tensor = tf.expand_dims(tensor, axis=0)  # Add batch dimension
        return tensor

    # Function to Predict Sign
    def predict_sign(frame):
        if model is None:
            return "Error: Model not loaded", 0.0
        processed_frame = preprocess_frame(frame)
        predictions = model.predict(processed_frame)
        pred_index = np.argmax(predictions[0])
        pred_class = index_to_class.get(pred_index, "Unknown")
        confidence = np.max(predictions[0]) * 100
        return pred_class, confidence

    # ---- STREAMLIT UI ----


    # Option to use Webcam or Upload Video
    option = st.radio("Choose input method:", ("Use Webcam", "Upload Video"))

    # Placeholder for displaying detected sign
    detected_sign_placeholder = st.empty()

    if option == "Use Webcam":
        st.write("Real-time Sign Language Recognition")
        st.warning("Press 'q' on your keyboard to stop the webcam.")

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

                    # Speak the predicted sign
                    cleaned_pred_class = pred_class.replace("_", " ")
                    speak_text(cleaned_pred_class)

                    # Update detected sign text box
                    cleaned_pred_class = pred_class.replace("_", " ")
                    detected_sign_placeholder.text(f"Detected Sign: {cleaned_pred_class}")

                    # Display Prediction
                    cv2.putText(frame, f'{pred_class} ({confidence:.2f}%)', (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                else:
                    cv2.putText(frame, "No Hands Detected", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                # Display Frame in Streamlit
                stframe.image(frame, channels="BGR")

                # Check for manual exit using keyboard key 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break  # Stop if 'q' is pressed

        cap.release()
        cv2.destroyAllWindows()

    elif option == "Upload Video":
        uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

        if uploaded_file is not None:
            # Save uploaded file
            with open("temp_video.mp4", "wb") as f:
                f.write(uploaded_file.read())

            st.video("temp_video.mp4")

            # Process Video
            cap = cv2.VideoCapture("temp_video.mp4")
            stframe = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Predict Sign
                pred_class, confidence = predict_sign(frame)

                # Speak the predicted sign
                cleaned_pred_class = pred_class.replace("_", " ")
                speak_text(cleaned_pred_class)

                # Update detected sign text box
                cleaned_pred_class = pred_class.replace("_", " ")
                detected_sign_placeholder.text(f"Detected Sign: {cleaned_pred_class}")

                # Display Prediction on Frame
                cv2.putText(frame, f'{pred_class} ({confidence:.2f}%)', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                stframe.image(frame, channels="BGR")

            cap.release()
