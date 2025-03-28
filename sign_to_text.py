import streamlit as st
from PIL import Image
from phrases import phrases
from sentences import sentences

def sign_to_text():
    col1, col2 = st.columns([1,1])
    if col1.button("phrases", key="phrases_btn"):
            st.session_state.page = "phrases"
    if col2.button("sentences", key="sentences_btn"):
            st.session_state.page = "sentences"
    if "page" in st.session_state:
        if st.session_state.page == "phrases":
            phrases()
        elif st.session_state.page == "sentences":
            sentences()
