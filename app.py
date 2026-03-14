import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, get_user_from_db, RECIPE_PROMPT

# הגדרה ראשונית - חובה
st.set_page_config(page_title="RecipeAI", layout="wide", initial_sidebar_state="collapsed")
apply_styles()

# --- לוגיקת כניסה ---
if 'user_email' not in st.session_state:
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>RecipeAI</h1>", unsafe_allow_html=True)
    email = st.text_input("אימייל לכניסה:", key="login_email")
    if email:
        name = get_user_from_db(email)
        if name:
            if st.button(f"כניסה לאלבום של {name}"):
                st.session_state.user_email, st.session_state.first_name = email.lower().strip(), name
                st.rerun()
        else:
            new_name = st.text_input("איך קוראים לך?")
            if st.button("יצירת אלבום"):
                st.session_state.user_email, st.session_state.first_name = email.lower().strip(), new_name
                st.rerun()
    st.stop()

# --- בר עליון ---
st.markdown(f'<div class="main-header"><h1 style="font-family:serif; font-size:22px;">ספר המתכונים של {st.session_state.first_name}</h1></div>', unsafe_allow_html=True)

# --- תפריט צדי (נפתח מה-3 פסים) ---
with st.sidebar:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    mode = st.radio("תפריט:", ["📚 כניסה לספר", "✨ הוספת מתכון"])
    if st.button("יציאה"):
        del st.session_state['user_email']
        st.rerun()

# --- הצגת תוכן ---
if mode == "✨ הוספת מתכון":
    st.markdown("### הוספת מתכון חדש")
    file = st.file_uploader("העלי תמונה", type=["jpg", "png", "jpeg"])
    if file and st.button("שמירה לספר"):
        with st.status("מנתח ושומר..."):
            model = setup_ai(st.secrets["GEMINI_API_KEY"])
            res = model.generate_content([RECIPE_PROMPT, PIL.Image.open(file)])
            save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, res.text.split('\n')[0], res.text, "כללי")
            st.success("נשמר!")
            st.balloons()
else:
    df = load_recipes_from_cloud(st.session_state.user_email)
    if df.empty:
        st.info("הספר ריק.")
    else:
        for _, row in df.iterrows():
            with st.expander(f"📖 {row['name']}"):
                st.markdown(f'<div class="recipe-card"><div style="white-space: pre-line;">{row["content"]}</div></div>', unsafe_allow_html=True)
