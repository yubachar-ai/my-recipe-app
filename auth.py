import streamlit as st
from logic import get_user_from_db

def show_login_page():
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>RecipeAI</h1>", unsafe_allow_html=True)
    email = st.text_input("אימייל לכניסה:", key="login_email")
    if email:
        name = get_user_from_db(email)
        if name:
            if st.button(f"כניסה לאלבום של {name}"):
                st.session_state.user_email = email.lower().strip()
                st.session_state.first_name = name
                st.rerun()
        else:
            new_name = st.text_input("איך קוראים לך?")
            if st.button("יצירת אלבום חדש"):
                st.session_state.user_email = email.lower().strip()
                st.session_state.first_name = new_name
                st.rerun()
    return False
