import streamlit as st
from PIL import Image
from phrases import phrases
from sentences import sentences
from text_to_sign import text_to_sign
from learn_sl import learn_sl
from quiz import quiz
from chatbot import chatbot

# Set page config
st.set_page_config(page_title="SignLoom - Silence Speaks", page_icon="👐", layout="wide")

# Logo path
logo_path = "logo.PNG"  # Ensure this is in the correct directory

# Sidebar Navigation
st.sidebar.image(logo_path, width=160)  # Display the logo in sidebar
st.sidebar.title("Navigation")

# Define Main Navigation Menu (Home as default)
menu_options = ["Home", "Sign-to-Text", "Text-to-Sign", "Tutor"]
main_menu = st.sidebar.radio("Select Section", menu_options, index=0)  # Home as default

# Home Page Content
if main_menu == "Home":
    # Custom Styling
    st.markdown(
        """
        <style>
            .header-container {
                display: flex;
                align-items: center;
                justify-content:space-between;
                gap: 15px;
                margin-bottom: 20px;
            }
            .title {
                font-size: 100px;
                font-weight: bold;
                background: linear-gradient(to right, #ff7675, #fdcb6e);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            .subtitle {
                font-size: 50px;
                color: #ff7675;
                margin: 0;
                white-space: nowrap;
                overflow: hidden;
                display: inline-block;
                position: relative;
                width: 100%;
                text-align: right;
            }
            .subtitle span {
                display: inline-block;
                position: relative;
                animation: bounce-text 3s ease-in-out infinite alternate;
            }
            @keyframes bounce-text {
                0% { transform: translateX(0%); }
                100% { transform: translateX(0%); }
            }
            .image-container {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 20px;
            }
            .animated-image {
                width: 100%;
                max-width: 300px;
                border-radius: 15px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                animation: fade-in 5s ease-in-out;
            }
            @keyframes fade-in {
                0% { opacity: 0; transform: scale(0.8); }
                100% { opacity: 1; transform: scale(1); }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Logo and Title Row Layout
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(logo_path, width=150)  # Adjust width for clarity
    with col2:
        st.markdown('<div class="title">SignLoom</div>', unsafe_allow_html=True)

    # Subtitle with bouncing effect
    st.markdown('<div class="subtitle"><span>Silence Speaks</span></div>', unsafe_allow_html=True)
     # Three Images Below Subtitle with Animation
    image_paths = ["image2.jpeg", "image1.jpeg", "image3.jpeg"]  # Replace with actual image paths
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(image_paths[0], use_container_width=True, caption="Sign-to-Text")
    with col2:
        st.image(image_paths[1], use_container_width=True, caption="Text-to-Sign")
    with col3:
        st.image(image_paths[2], use_container_width=True, caption="Learn Sign Language")


elif main_menu == "Sign-to-Text":
    sub_menu = st.sidebar.radio("Options", ["Phrases", "Sentences"])
    if sub_menu == "Phrases":
        st.title("Sign-to-Text: Phrases")
        phrases()
    elif sub_menu == "Sentences":
        st.title("Sign-to-Text: Sentences")
        sentences()

elif main_menu == "Text-to-Sign":
    st.title("Text-to-Sign")
    text_to_sign()

elif main_menu == "Tutor":
    sub_menu = st.sidebar.radio("Options", ["Learn Sign", "Quiz"])
    if sub_menu == "Learn Sign":
        learn_sl()
    elif sub_menu == "Quiz":
        st.title("Sign Language Quiz")
        quiz()

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Choose an option to proceed.")
