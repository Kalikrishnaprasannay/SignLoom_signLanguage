import streamlit as st
from PIL import Image
import random
import streamlit.components.v1 as components
from learn_sl import learn_sl
from quiz import quiz
def tutor():
    col1, col2 = st.columns([1,1])
    if col1.button("learn_sl", key="learn_sl_btn"):
            st.session_state.page = "learn_sl"
    if col2.button("quiz", key="quiz_btn"):
            st.session_state.page = "quiz"
    if "page" in st.session_state:
        if st.session_state.page == "learn_sl":
            learn_sl()
        elif st.session_state.page == "quiz":
            quiz()
