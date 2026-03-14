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
import streamlit.components.v1 as components

# --- בתוך app.py, בחלק של ה-else (מצב אלבום) ---
else:
    df = load_recipes_from_cloud(st.session_state.user_email)
    
    if 'page_index' not in st.session_state:
        st.session_state.page_index = 0

    if df.empty:
        st.info("האלבום שלך עדיין ריק.")
    else:
        total_pages = len(df) + 1 
        current_idx = st.session_state.page_index

        # הצגת התוכן
        if current_idx == 0:
            st.markdown(f"""
                <div class='book-cover'>
                    <h4 style='font-family: serif; font-weight: normal;'>DIGITAL HEIRLOOM</h4>
                    <h1 style='color: white; font-size: 42px;'>{st.session_state.first_name}</h1>
                    <div style='margin: 30px 0; font-size: 40px;'>📖</div>
                    <p style='font-size: 14px; opacity: 0.8;'>החליקי ימינה או שמאלה כדי לדפדף</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            recipe = df.iloc[current_idx - 1]
            st.markdown(f"""
                <div class='recipe-page'>
                    <p style='color: #BC8F8F; font-size: 12px; letter-spacing: 1px;'>{recipe.get('category', 'כללי')} | {recipe.get('date', '')}</p>
                    <h1 style='font-family: "Playfair Display", serif; font-size: 32px; margin-bottom: 20px;'>{recipe['name']}</h1>
                    <div style='border-top: 1px solid #f0f0f0; padding-top: 20px; font-size: 17px; color: #2D2926;'>
                        {recipe['content']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # --- רכיב ה-Swipe (JavaScript נסתר) ---
        # הקוד הזה מזהה החלקה ומפעיל את הכפתורים של סטרימליט
        swipe_js = f"""
        <script>
        var startX;
        document.addEventListener('touchstart', function(e) {{
            startX = e.touches[0].clientX;
        }}, false);
        
        document.addEventListener('touchend', function(e) {{
            var endX = e.changedTouches[0].clientX;
            var diffX = startX - endX;
            if (Math.abs(diffX) > 50) {{
                if (diffX > 0) {{
                    window.parent.postMessage({{type: 'streamlit:set_widget_value', key: 'next_page', value: true}}, '*');
                }} else {{
                    window.parent.postMessage({{type: 'streamlit:set_widget_value', key: 'prev_page', value: true}}, '*');
                }}
            }}
        }}, false);
        </script>
        """
        components.html(swipe_js, height=0)

        # כפתורי ניווט נסתרים (ה-JS לוחץ עליהם עבורנו)
        col_prev, col_page, col_next = st.columns([1, 2, 1])
        with col_prev:
            if current_idx > 0:
                if st.button("➡️ הקודם", key="prev_btn"):
                    st.session_state.page_index -= 1
                    st.rerun()
        with col_page:
            st.markdown(f"<p style='text-align: center; color: #999;'>{current_idx + 1} / {total_pages}</p>", unsafe_allow_html=True)
        with nav_col3: # וודאי שזה תואם לשם הטור שלך
             if current_idx < total_pages - 1:
                if st.button("הבא ⬅️", key="next_btn"):
                    st.session_state.page_index += 1
                    st.rerun()
