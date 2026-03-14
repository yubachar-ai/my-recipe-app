import streamlit as st
from styles import apply_styles
from auth import show_login_page
from pages_content import show_add_recipe, show_my_book

# 1. הגדרות בסיס - חובה להגדיר שהתפריט הצדי יהיה סגור בהתחלה (collapsed)
st.set_page_config(
    page_title="RecipeAI", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)
apply_styles()

# 2. בדיקת כניסה
if 'user_email' not in st.session_state:
    show_login_page()
    st.stop()

# 3. בר עליון קבוע (ללא התפריט)
st.markdown(f'<div class="main-header"><h1 class="header-title">ספר המתכונים של {st.session_state.first_name}</h1></div>', unsafe_allow_html=True)

# 4. התפריט שיופיע רק בתוך ה-3 פסים (Sidebar)
with st.sidebar:
    st.markdown("<br><br><br>", unsafe_allow_html=True) # רווח מלמעלה
    st.markdown("### תפריט ניווט")
    
    # זה הקוד שיושב בתוך ה-Sidebar ולא באמצע המסך
    mode = st.radio(
        "לאן לעבור?",
        ["📚 הספר שלי", "✨ הוספת מתכון"],
        label_visibility="collapsed" # מחביא את הכותרת של הרדיו למראה נקי
    )
    
    st.markdown("---")
    if st.button("יציאה מהחשבון"):
        del st.session_state['user_email']
        st.rerun()

# 5. הצגת הדף הנבחר בשטח המרכזי
if mode == "✨ הוספת מתכון":
    show_add_recipe()
else:
    show_my_book()
