🤟 SignLoom - Real-Time Sign Language Interpreter


🚀 Overview
SignLoom is a real-time sign language interpreter designed to bridge communication gaps for the deaf and hard-of-hearing community. Using deep learning, computer vision, and a user-friendly interface, it translates sign language gestures into text and speech instantly.

The system is built with MobileNetV2, MediaPipe, OpenCV, and Streamlit, and features both a real-time sign detection module and an interactive tutor to help users learn sign language.

🧠 Problem Statement
Millions of people face daily communication barriers due to hearing disabilities. Traditional methods like lip-reading or note writing are slow and insufficient. Existing sign translation systems often lack real-time performance, accuracy, or accessibility. SignLoom addresses these issues head-on.

🎯 Key Features
🎥 Real-time webcam sign recognition

🧠 Transfer learning using MobileNetV2

📦 Custom-trained model with 3000+ gesture images

🔄 Live Sign ➜ Text ➜ Speech

🧑‍🏫 Sign Language Tutor with:

Alphabet, number, and phrase learning

Interactive quizzes

Visual and auditory feedback

📄 Sentence recognition with start/stop gestures

🧩 GIF generation for sentence formation

🔤 Text-to-Sign translation using mapping logic

👨‍🏫 For Whom?
Deaf and mute individuals

Friends, family, and educators

Healthcare professionals

Emergency responders

Anyone interested in learning sign language

🔧 Tech Stack

Category | Technology,

Model & Training | TensorFlow, Keras, MobileNetV2,

Hand Detection | MediaPipe

Real-Time Video Capture | OpenCV

Frontend UI | Streamlit

Audio Output | pyttsx3 (Text to Speech)

Data Processing | NumPy, PIL, Scikit-learn

Gesture Augmentation | ImageDataGenerator


🏗️ System Architecture
1.Capture frames from webcam using OpenCV.

2.Detect hand landmarks via MediaPipe.

3.Preprocess ROI and feed to MobileNetV2 model.

4.Display prediction and confidence.

5.Output translated text and speech.

6.Tutor module for visual learning and quizzes.

📈 Results
📊 Achieved 94% accuracy on validation data

⚡ Real-time prediction within 1–2 seconds

🧪 Tested across varied environments for robustness

🧩 Supports individual signs and sentence-level input

🧠 Tutor quizzes show enhanced user learning retention

📹 Demo
🎥 Watch our final working demo here:

🎥 [Watch Final Demo](videos/final_demo_team_8056.mp4)


📌 Future Scope
📱 Android/iOS app integration

🌐 Support for BSL, ISL, and other regional signs

🧑‍🎤 Facial expression recognition

🤖 LSTM-based sentence construction

🧍‍♂️ Virtual avatar for text-to-sign conversion

📡 Cloud API for wider integration

🧩 Gamified learning modules


👥 Team

Rudraraju Srihita 

Kalikrishna Prasanna Y





🌍 Let's build a more inclusive world, one gesture at a time. ✨

