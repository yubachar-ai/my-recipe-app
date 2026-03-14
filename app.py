import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, get_user_from_db, RECIPE_PROMPT

st.set_page_config(page_title="RecipeAI", layout="centered")
apply_styles()

# --- כניסה ---
if 'user_email' not in st.session_state:
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>RecipeAI</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email = st.text_input("אימייל:", key="login_email")
        if email:
            name = get_user_from_db(email)
            if name and st.button(f"כניסה לאלבום של {name}"):
                st.session_state.user_email = email.lower().strip()
                st.session_state.first_name = name
                st.rerun()
            elif email:
                new_name = st.text_input("איך קוראים לך?")
                if st.button("הרשמה"):
                    st.session_state.user_email = email.lower().strip()
                    st.session_state.first_name = new_name
                    st.rerun()
    st.stop()

# --- בר עליון קבוע ---
st.markdown(f"""
    <div class="main-header">
        <h1 class="header-title">ספר המתכונים של {st.session_state.first_name}</h1>
    </div>
""", unsafe_allow_html=True)

# --- תפריט צדי (בלבד!) ---
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### ניווט")
    # כאן התיקון הקריטי: השימוש ב-st.sidebar
    mode = st.sidebar.radio(
        "בחרי פעולה:",
        ["📚 כניסה לספר", "✨ הוספת מתכון"],
        label_visibility="collapsed" # מסתיר את הכותרת הכפולה
    )
    st.markdown("---")
    if st.sidebar.button("יציאה מהחשבון"):
        del st.session_state['user_email']
        st.rerun()

# --- שטח התוכן ---
if mode == "✨ הוספת מתכון":
    st.markdown("### ✨ הוספת מתכון חדש")
    file = st.file_uploader("צלמי או העלי תמונה", type=["jpg", "png", "jpeg"])
    if file and st.button("שמירה לספר ✨"):
        with st.status("ה-AI מנתח ושומר..."):
            model = setup_ai(st.secrets["GEMINI_API_KEY"])
            res = model.generate_content([RECIPE_PROMPT, PIL.Image.open(file)])
            save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, res.text.split('\n')[0], res.text, "כללי")
            st.success("נשמר!")
            st.balloons()

else:
    df = load_recipes_from_cloud(st.session_state.user_email)
    if df.empty:
        st.info("הספר ריק. זמן למלא אותו!")
    else:
        search = st.text_input("🔍 חפשי מתכון...", placeholder="מה בא לך לבשל?")
        if search:
            df = df[df['name'].str.contains(search, case=False, na=False)]
            
        for _, row in df.iterrows():
            with st.expander(f"📖 {row['name']}"):
                st.markdown(f"""
                    <div class="recipe-card">
                        <div style="white-space: pre-line;">{row['content']}</div>
                    </div>
                """, unsafe_allow_html=True)
