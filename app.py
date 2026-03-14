import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, get_user_from_db, RECIPE_PROMPT

st.set_page_config(page_title="RecipeAI", page_icon="👩‍🍳", layout="wide")
apply_styles()

# ניהול מצבי כניסה (Session State)
if 'user_email' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>ברוכה הבאה ל-RecipeAI</h1>", unsafe_allow_html=True)
    
    # שלב 1: הזנת מייל
    email_input = st.text_input("הקלידי אימייל לכניסה:", placeholder="email@example.com")
    
    if email_input:
        # בדיקה אם המשתמש קיים בבסיס הנתונים
        existing_name = get_user_from_db(email_input)
        
        if existing_name:
            st.success(f"שמחים שחזרת, {existing_name}!")
            if st.button(f"כניסה לאלבום של {existing_name}"):
                st.session_state.user_email = email_input.lower().strip()
                st.session_state.first_name = existing_name
                st.rerun()
        else:
            # שלב 2: משתמש חדש - שואלים שם
            st.info("נראה שזו פעם ראשונה שלך! איך קוראים לך?")
            new_name = st.text_input("שם פרטי:", placeholder="השם שלך...")
            if st.button("יצירת אלבום וכניסה"):
                if new_name:
                    st.session_state.user_email = email_input.lower().strip()
                    st.session_state.first_name = new_name
                    st.rerun()
    st.stop()

# --- מכאן והלאה הקוד של האפליקציה (זהה לקוד הקודם) ---
api_key = st.secrets["GEMINI_API_KEY"]
model = setup_ai(api_key.strip())

with st.sidebar:
    st.title(f"היי {st.session_state.first_name}! 👋")
    mode = st.radio("לאן הולכים?", ["📚 דפדוף באלבום", "✨ סריקת מתכון חדש"])
    if st.button("החלפת משתמש / יציאה"):
        del st.session_state['user_email']
        st.rerun()

if mode == "✨ סריקת מתכון חדש":
    st.header("סריקת מתכון חדש")
    uploaded_file = st.file_uploader("צלמי או העלי תמונה", type=["jpg", "png", "jpeg"])
    category = st.selectbox("לאיזו קטגוריה זה שייך?", ["🥗 סלטים", "🍰 קינוחים", "🍝 עיקריות", "🥐 מאפים", "🍲 מרקים"])
    
    if uploaded_file and st.button("שמור לאלבום ✨"):
        with st.status("מנתח ושומר...") as status:
            img = PIL.Image.open(uploaded_file)
            response = model.generate_content([RECIPE_PROMPT, img])
            full_text = response.text
            recipe_name = full_text.split('\n')[0].replace('#','').strip()
            save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, recipe_name, full_text, category)
            status.update(label="נשמר באלבום!", state="complete")
            st.balloons()
else:
    st.header(f"האלבום של {st.session_state.first_name}")
    df = load_recipes_from_cloud(st.session_state.user_email)
    if not df.empty:
        for i, row in df.iterrows():
            with st.expander(f"📖 {row['name']} ({row.get('date', '')})"):
                st.markdown(f"<div class='recipe-card'>{row['content']}</div>", unsafe_allow_html=True)
    else:
        st.info("האלבום עדיין ריק. לכי לסריקה!")
