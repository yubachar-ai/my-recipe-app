import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, get_user_from_db, RECIPE_PROMPT

# הגדרות עמוד
st.set_page_config(page_title="RecipeAI", layout="wide")
apply_styles()

# תמונות אווירה יוקרתיות
HERO_IMAGE = "https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=2070&auto=format&fit=crop"
BOOK_IMAGE = "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?q=80&w=2070&auto=format&fit=crop"
SCAN_IMAGE = "https://images.unsplash.com/photo-1505935428862-770b6f24f629?q=80&w=2067&auto=format&fit=crop"

# --- מסך כניסה ---
if 'user_email' not in st.session_state:
    st.image(HERO_IMAGE, use_container_width=True)
    st.markdown("<h1 style='text-align: center;'>RecipeAI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>הופכים זיכרונות משפחתיים לנכס דיגיטלי</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email = st.text_input("אימייל לכניסה:", placeholder="שם@מייל.קום")
        if email:
            name = get_user_from_db(email)
            if name:
                st.markdown(f"<div style='text-align: right;'>שלום <b>{name}</b>, איזה כיף שחזרת!</div>", unsafe_allow_html=True)
                if st.button("כניסה לספר שלי"):
                    st.session_state.user_email = email.lower().strip()
                    st.session_state.first_name = name
                    st.rerun()
            else:
                st.markdown("<div style='text-align: right;'>נראה שזו פעם ראשונה! איך קוראים לך?</div>", unsafe_allow_html=True)
                new_name = st.text_input("שם פרטי:")
                if st.button("יצירת אלבום אישי"):
                    if new_name:
                        st.session_state.user_email = email.lower().strip()
                        st.session_state.first_name = new_name
                        st.rerun()
    st.stop()

# --- אתחול מודל AI ---
api_key = st.secrets["GEMINI_API_KEY"]
model = setup_ai(api_key.strip())

# --- ניווט (Sidebar) ---
with st.sidebar:
    st.markdown(f"<div style='text-align: right;'><h3>שלום {st.session_state.first_name}</h3></div>", unsafe_allow_html=True)
    mode = st.radio("תפריט:", ["📚 האלבום שלי", "✨ סריקת מתכון"])
    st.markdown("---")
    if st.button("יציאה מהחשבון"):
        del st.session_state['user_email']
        st.rerun()

# --- מצב סריקה ---
if mode == "✨ סריקת מתכון":
    st.markdown("<h1 style='text-align: right;'>סריקה חכמה</h1>", unsafe_allow_html=True)
    st.image(SCAN_IMAGE, use_container_width=True)
    
    file = st.file_uploader("העלי תמונה של המתכון", type=["jpg", "png", "jpeg"])
    cat = st.selectbox("לאיזו קטגוריה לשייך?", ["🥗 סלטים", "🍰 קינוחים", "🍝 עיקריות", "🥐 מאפים", "🍲 מרקים"])
    
    if file and st.button("שמירה לאלבום ✨"):
        with st.status("ה-AI מנתח את המתכון...", expanded=True) as status:
            img = PIL.Image.open(file)
            res = model.generate_content([RECIPE_PROMPT, img])
            full_text = res.text
            recipe_name = full_text.split('\n')[0].replace('#','').strip()
            save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, recipe_name, full_text, cat)
            status.update(label="נשמר בהצלחה!", state="complete")
            st.balloons()
            st.rerun()

# --- מצב אלבום ---
else:
    st.markdown(f"<h1 style='text-align: right;'>האלבום של {st.session_state.first_name}</h1>", unsafe_allow_html=True)
    st.image(BOOK_IMAGE, use_container_width=True)
    
    df = load_recipes_from_cloud(st.session_state.user_email)
    
    if not df.empty:
        # סרגל חיפוש בעברית
        search = st.text_input("🔍 חפשי מתכון...", placeholder="מה בא לך לבשל?")
        if search:
            df = df[df['name'].str.contains(search, case=False, na=False)]
            
        for i, row in df.iterrows():
            with st.expander(f"📖 {row['name']} | {row.get('date', '')}"):
                st.markdown(f"<div class='recipe-card'>{row['content']}</div>", unsafe_allow_html=True)
    else:
        st.info("עדיין אין מתכונים באלבום. זמן להתחיל לסרוק!")
