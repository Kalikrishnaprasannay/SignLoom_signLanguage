import os
import base64
import streamlit as st
from PIL import Image
import speech_recognition as sr

def text_to_sign():
    # Path to dataset
    DATASET_PATH = "./Words"

    recognizer = sr.Recognizer()

    def recognize_speech():
        with sr.Microphone() as source:
            with st.spinner("Listening..."):
                audio_data = recognizer.listen(source)
            try:
                return recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                st.error("Could not understand the audio")
            except sr.RequestError:
                st.error("Could not request results, please try again")
        return ""

    # Convert English to Sign Language Order
    def convert_to_sign_language(text):
        mapping = {"Me want food" : "I want food", "You have My Book" : "Me book you have",
                "He can play": "He play", "She like my friend" : "She like me friend",
                "It is small" : "It small", "We know Sign Language" : "We know SignLanguage",
                "your car is good" : "You car good", "It is my house" : "My house it",
                "I love You" : "Love you me", "You like my car" : "You like me car",
                    "We learn sign langauge" : "We learn SignLnguage", "They have money" : "They have money",
                    "I know your name" : "I know your name", "She want help" : "She want help",
                    "He can write" : "He can write", "Please give me food" : "Food give me please",
                    "You take my Phone" : "Me phone you take", "We help you" : "We help you",
                    "Come to my house" : "me house come", "They go to school" : "School they go",
                    "I read book" : "Book me read", "You write now" : "now you write",
                    "I sleep at night" : "Me sleep night", "I feel sad" : "sad Me feel",
                    "we meet again" : "again we meet", "they play now" : "now they play",
                    "You are my friend" : "friend you me", "my house is small" : "Me house small",
                    "I learn sign language" : "Me learn SignLangauge", "what is your name" : "you name what",
                    "I feel happy" : "Me fell happy", "that is right" : "that right",
                    "you are good" : "you good", "when do we meet" : "we meet when",
                    "why are you sad" : "you sad why", "how do we start" : "we start how",
                    "what is this" : "it what", "plesae read that again" : "read again please",
                    "Please help me" : "help me please", "thank you for help" : "help thankyou",
                    "yes i know" : "me know yes", "no it is wrong" : "no it wrong",
                    "He want your answer" : "he want you answer", "she can read and write" : "she can read write",
                    "she know sign language" : "she know sign language", "they know where we go" : "they know we go where",
                    "you feel my sad" : "my sad you feel", "it is bad stop now" : "stop now it  bad",
                    "my friend want your help" : "me friend want you help", "i have good food" : "Me have good food",
                    "they play at night" : "night they play", "we learn when they come" : "when they come we learn",
                    "he write in my book" : "me book he write", "she take the money" : "money she take",
                    "you give me time" : "time you give me", "it is right yes" : "yes it right",
                    "why you sleep in day" : "you sleep day why", "how they know my name" : "me name they know how",
                    "what time we meet" : "we meet time what", "where is your school" : "you school where",
                    "please come again" : "come again please", "stop your bad play" : "you bad play stop",
                    "start the car now" : "start car now", "give me the good answer" : "good answer give me",
                    "i have small car" : "me have small car", "i know your school is good" : "you school good i know",
                    "the food is good i like it" : "food good me like it", "help me to learn sign language " : "help me learn sign language ",
                    "i want to know her name" : "she name me want know", "where did you learn sign language " : "you learn signlanguage where",
                    "please read his answer" : "read he answer please", " you give me time i will help you" : "me help you give me time ",
                    "when did it started" : "it start when when", "why do you want my book" : "you want me book why",
                    "why she want to know my answer" : "she want to know me answer why", "we feel happy when we go to play" : "when we go play we feel happy",
                    "if we help them they will give us money" : "we help they give money we", "give me time i learn sign language" : "me learn signlanguage give time",
                    "she need time" : "she want time", "we have money" : "money we have",
                    "they start now" : "they start now", "we feel happy" : "happy we feel",
                    "how to go school" : "go school how", "he like book" : "book he like",
                    "how do you know" : "you know how", "can i help you" : "help you can me",
                    "she takes time" : "she take time", "they have my money" : "me money they have",
                    "she helps me " : "ahe help me", "she likes to learn" : "learn she like",
                    "take your time and give the answer" : "you take time give answer", "this is a good book" : "good book",
                    "you come and help me" : "you come help me", "help me to write answer" : "help me write answer",
                    "sorry i go home now" : "sorry me go house now", "we write answer in the book" : "we write answer book",
                    "where did you go" : "you go where", "why did you gave me the book " : "you give book me why",
                    "at what time you will come" : "you come what time", "when did you called me" : "you phone me when",
                    "take your own time" : "you take time", "we shall play now" : "we play now", }  # Extend this dictionary
        return mapping.get(text.lower(), text.lower())

    # Ensure session states exist
    if "recognized_text" not in st.session_state:
        st.session_state["recognized_text"] = ""
    if "manual_text" not in st.session_state:
        st.session_state["manual_text"] = ""
    if "sign_language_text" not in st.session_state:
        st.session_state["sign_language_text"] = ""

    def handle_manual_text():
        if st.session_state.manual_text:
            st.session_state.sign_language_text = convert_to_sign_language(st.session_state.manual_text)
            st.session_state.manual_text = ""  # Clear input box
            st.session_state.recognized_text = ""  # Hide recognized text

    def handle_audio_input():
        speech_text = recognize_speech()
        if speech_text:
            st.session_state.recognized_text = speech_text
            st.session_state.sign_language_text = convert_to_sign_language(speech_text)

    # Layout for text input and record button
    col1, col2 = st.columns([1, 1])

    with col1:
        st.text_input("Enter text:", value=st.session_state.manual_text, key="manual_text", on_change=handle_manual_text)

    with col2:
        st.markdown("<div style='margin-top: 29px;'></div>", unsafe_allow_html=True)  # Adjusting position
        if st.button("🎤"):
            handle_audio_input()

    # Display Recognized Text (Only for Audio Input)
    if st.session_state["recognized_text"]:
        st.markdown(f'<div style="font-size:18px; font-weight:bold; color:blue;">Recognized Text: {st.session_state["recognized_text"]}</div>', unsafe_allow_html=True)

    # Display Sign Language Text
    st.markdown(f'<div style="font-size:20px; font-weight:bold; color:green;">Sign Language Text: {st.session_state["sign_language_text"]}</div>', unsafe_allow_html=True)

    # Process Sign Language Words
    words = st.session_state["sign_language_text"].split()
    valid_words = [word for word in words if os.path.exists(os.path.join(DATASET_PATH, word))]

    # Function to get frames for a word
    def get_frames_for_word(word):
        folder_path = os.path.join(DATASET_PATH, word)
        if not os.path.exists(folder_path):
            return []

        preferred_videos = ["video_1", "video_2"]
        selected_video = None

        for video in preferred_videos:
            video_path = os.path.join(folder_path, video)
            if os.path.exists(video_path):
                selected_video = video_path
                break

        if not selected_video:
            return []

        frame_files = sorted(os.listdir(selected_video))
        frame_files = [os.path.join(selected_video, f) for f in frame_files if f.endswith((".jpg", ".png"))]

        return frame_files

    # Function to create an animated GIF
    def create_animated_gif(frames, output_path="animated_output.gif", duration=150):
        if not frames:
            return None

        images = [Image.open(frame).convert("RGB") for frame in frames]  # Ensure images are RGB
        images[0].save(output_path, save_all=True, append_images=images[1:], format="GIF", duration=duration, loop=0)
        return output_path

    # Function to encode GIF as Base64
    def get_base64_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # Collect frames for all valid words
    all_frames = []
    for word in valid_words:
        all_frames.extend(get_frames_for_word(word))

    # Generate animated GIF if frames exist
    if all_frames:
        gif_path = create_animated_gif(all_frames)
        base64_gif = get_base64_image(gif_path)

        st.markdown(f'<img src="data:image/gif;base64,{base64_gif}" alt="Generated GIF" style="border-radius: 10px; margin-top: 15px; display: block; margin-left: auto; margin-right: auto;">', unsafe_allow_html=True)

        with open(gif_path, "rb") as file:
            st.download_button("Download Animated GIF", file, file_name="sign_language.gif", mime="image/gif")
    else:
        st.error("No matching sign words found. Try another input.")
