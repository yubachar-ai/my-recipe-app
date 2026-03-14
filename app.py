import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, get_user_from_db, RECIPE_PROMPT

st.set_page_config(page_title="RecipeAI", layout="wide")
apply_styles()

# תמונת אווירה ראשית (Rustic Kitchen)
HERO_IMAGE = "https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=2070&auto=format&fit=crop"
BOOK_IMAGE = "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?q=80&w=2070&auto=format&fit=crop"

if 'user_email' not in st.session_state:
    st.image("https://...", use_container_width=True)
    st.markdown("<h1 style='text-align: center;'>RecipeAI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>הופכים זיכרונות משפחתיים לנכס דיגיטלי</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email = st.text_input("אימייל לכניסה:", placeholder="שם@מייל.קום")
        if email:
            name = get_user_from_db(email)
            if name:
                st.markdown(f"<p style='text-align: center;'>שלום <b>{name}</b>, איזה כיף שחזרת!</p>", unsafe_allow_html=True)
                if st.button("כניסה לספר שלי"):
                    st.session_state.user_email = email.lower().strip()
                    st.session_state.first_name = name
                    st.rerun()
            else:
                new_name = st.text_input("נראה שזו פעם ראשונה! איך קוראים לך?")
                if st.button("יצירת אלבום אישי"):
                    if new_name:
                        st.session_state.user_email = email.lower().strip()
                        st.session_state.first_name = new_name
                        st.rerun()
    st.stop()

# ניווט
with st.sidebar:
    st.markdown(f"<h2 style='text-align: right;'>שלום {st.session_state.first_name}</h2>", unsafe_allow_html=True)
    mode = st.radio("תפריט:", ["📚 האלבום שלי", "✨ סריקת מתכון"])

if mode == "✨ סריקת מתכון":
    st.markdown("<h1 style='text-align: right;'>סריקה חכמה</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1505935428862-770b6f24f629?q=80&w=2067&auto=format&fit=crop", class_name="hero-img")
    
    file = st.file_uploader("העלי תמונה של המתכון", type=["jpg", "png", "jpeg"])
    cat = st.selectbox("קטגוריה", ["🥗 סלטים", "🍰 קינוחים", "🍝 עיקריות", "🥐 מאפים", "🍲 מרקים"])
    
    if file and st.button("שמירה לאלבום"):
        with st.status("ה-AI מנתח את המתכון..."):
            model = setup_ai(st.secrets["GEMINI_API_KEY"])
            img = PIL.Image.open(file)
            res = model.generate_content([RECIPE_PROMPT, img])
            save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, res.text.split('\n')[0], res.text, cat)
            st.balloons()
            st.rerun()

else:
    st.markdown(f"<h1 style='text-align: right;'>האלבום של {st.session_state.first_name}</h1>", unsafe_allow_html=True)
    st.image(BOOK_IMAGE, class_name="hero-img")
    
    df = load_recipes_from_cloud(st.session_state.user_email)
    if not df.empty:
        for i, row in df.iterrows():
            with st.expander(f"📖 {row['name']}"):
                st.markdown(f"<div class='recipe-card'>{row['content']}</div>", unsafe_allow_html=True)
    else:
        st.info("עדיין אין מתכונים באלבום. זמן להתחיל לסרוק!")
