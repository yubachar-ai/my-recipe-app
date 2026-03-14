import streamlit as st
import PIL.Image
import streamlit.components.v1 as components
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, get_user_from_db, RECIPE_PROMPT

# הגדרות עמוד
st.set_page_config(page_title="RecipeAI", layout="wide")
apply_styles()

# תמונות אווירה
HERO_IMAGE = "https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=2070&auto=format&fit=crop"

# ניהול כניסה
if 'user_email' not in st.session_state:
    st.image(HERO_IMAGE, use_container_width=True)
    st.markdown("<h1 style='text-align: center;'>RecipeAI</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email = st.text_input("אימייל לכניסה:", placeholder="email@example.com")
        if email:
            name = get_user_from_db(email)
            if name:
                st.markdown(f"<div style='text-align: right;'>שלום <b>{name}</b></div>", unsafe_allow_html=True)
                if st.button("כניסה לספר שלי"):
                    st.session_state.user_email = email.lower().strip()
                    st.session_state.first_name = name
                    st.rerun()
            else:
                new_name = st.text_input("איך קוראים לך?")
                if st.button("יצירת אלבום אישי"):
                    if new_name:
                        st.session_state.user_email = email.lower().strip()
                        st.session_state.first_name = new_name
                        st.rerun()
    st.stop()

# אתחול AI
api_key = st.secrets["GEMINI_API_KEY"]
model = setup_ai(api_key.strip())

# ניווט (Sidebar)
with st.sidebar:
    st.markdown(f"<div style='text-align: right;'><h3>שלום {st.session_state.first_name}</h3></div>", unsafe_allow_html=True)
    mode = st.radio("תפריט:", ["📚 האלבום שלי", "✨ סריקת מתכון"])
    st.markdown("---")
    if st.button("יציאה"):
        del st.session_state['user_email']
        st.rerun()

# --- לוגיקת האפליקציה ---

if mode == "✨ סריקת מתכון":
    st.markdown("<h1 style='text-align: right;'>סריקה חכמה</h1>", unsafe_allow_html=True)
    file = st.file_uploader("העלי תמונה", type=["jpg", "png", "jpeg"])
    cat = st.selectbox("קטגוריה", ["🥗 סלטים", "🍰 קינוחים", "🍝 עיקריות", "🥐 מאפים", "🍲 מרקים"])
    
    if file and st.button("שמירה לאלבום ✨"):
        with st.status("מנתח ושומר..."):
            img = PIL.Image.open(file)
            res = model.generate_content([RECIPE_PROMPT, img])
            recipe_name = res.text.split('\n')[0].replace('#','').strip()
            save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, recipe_name, res.text, cat)
            st.balloons()
            st.rerun()

else:
    # --- מצב אלבום (הספר הדיגיטלי) ---
    df = load_recipes_from_cloud(st.session_state.user_email)
    
    if 'page_index' not in st.session_state:
        st.session_state.page_index = 0

    if df.empty:
        st.info("האלבום שלך עדיין ריק. זמן להתחיל לסרוק!")
    else:
        total_pages = len(df) + 1 
        current_idx = st.session_state.page_index

        # הצגת התוכן (כריכה או מתכון)
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
                    <p style='color: #BC8F8F; font-size: 12px;'>{recipe.get('category', 'כללי')} | {recipe.get('date', '')}</p>
                    <h1 style='font-family: serif; font-size: 32px;'>{recipe['name']}</h1>
                    <div style='border-top: 1px solid #f0f0f0; padding-top: 20px;'>
                        {recipe['content']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # רכיב ה-Swipe (JavaScript)
        swipe_js = """
        <script>
        var startX;
        document.addEventListener('touchstart', function(e) { startX = e.touches[0].clientX; }, false);
        document.addEventListener('touchend', function(e) {
            var endX = e.changedTouches[0].clientX;
            var diffX = startX - endX;
            if (Math.abs(diffX) > 50) {
                const btn = (diffX > 0) ? window.parent.document.querySelector('button[kind="secondary"]:last-child') 
                                      : window.parent.document.querySelector('button[kind="secondary"]:first-child');
                if (btn) btn.click();
            }
        }, false);
        </script>
        """
        components.html(swipe_js, height=0)

        # כפתורי ניווט
        st.markdown("<br>", unsafe_allow_html=True)
        col_p, col_c, col_n = st.columns([1, 2, 1])
        with col_p:
            if current_idx > 0:
                if st.button("➡️ הקודם"):
                    st.session_state.page_index -= 1
                    st.rerun()
        with col_c:
            st.markdown(f"<p style='text-align: center;'>{current_idx + 1} / {total_pages}</p>", unsafe_allow_html=True)
        with col_n:
            if current_idx < total_pages - 1:
                if st.button("הבא ⬅️"):
                    st.session_state.page_index += 1
                    st.rerun()
