import streamlit as st
from styles import apply_styles
from auth import show_login_page
from pages_content import show_add_recipe, show_my_book

# 1. הגדרות בסיס
st.set_page_config(page_title="RecipeAI", layout="wide", initial_sidebar_state="collapsed")
apply_styles()

# 2. בדיקת כניסה
if 'user_email' not in st.session_state:
    show_login_page()
    st.stop()

# 3. בר עליון ותפריט צדי
st.markdown(f'<div class="main-header"><h1 style="font-family:serif; font-size:22px;">ספר המתכונים של {st.session_state.first_name}</h1></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    mode = st.radio("ניווט:", ["📚 כניסה לספר", "✨ הוספת מתכון"])
    if st.button("יציאה מהחשבון"):
        del st.session_state['user_email']
        st.rerun()

# 4. הצגת הדף הנבחר
if mode == "✨ הוספת מתכון":
    show_add_recipe()
else:
    show_my_book()
