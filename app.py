import streamlit as st
from styles import apply_styles
from auth import show_login_page
from pages_content import show_add_recipe, show_my_book

# הגדרה שתופסת את המרכז ומנקה את הצדדים
st.set_page_config(
    page_title="RecipeAI", 
    layout="centered", # שיניתי ל-centered בשביל יציבות בטלפון
    initial_sidebar_state="collapsed"
)
apply_styles()

if 'user_email' not in st.session_state:
    show_login_page()
    st.stop()

# בר עליון
st.markdown(f'<div class="main-header"><h1 class="header-title">ספר המתכונים של {st.session_state.first_name}</h1></div>', unsafe_allow_html=True)

# תפריט (Sidebar)
with st.sidebar:

    st.markdown("### תפריט")

    mode = st.radio(

        ["📚 הספר שלי", "✨ הוספת מתכון"],
        label_visibility="collapsed"
    )

    if st.button("יציאה מהחשבון"):
        del st.session_state['user_email']
        st.rerun()


# תוכן
if mode == "✨ הוספת מתכון":
    show_add_recipe()
else:
    show_my_book()
