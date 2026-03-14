import streamlit as st
import PIL.Image
import json
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, get_user_from_db, RECIPE_PROMPT

st.set_page_config(page_title="RecipeAI", layout="wide")
apply_styles()

if 'user_email' not in st.session_state:
    # --- מסך כניסה (נשאר אותו דבר) ---
    st.markdown("<h1 style='text-align: center; margin-top: 100px;'>RecipeAI</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email = st.text_input("אימייל:", key="login_email")
        if email:
            name = get_user_from_db(email)
            if name and st.button(f"כניסה לאלבום של {name}"):
                st.session_state.user_email, st.session_state.first_name = email, name
                st.rerun()
            elif not name and email:
                new_name = st.text_input("איך קוראים לך?")
                if st.button("הרשמה"):
                    st.session_state.user_email, st.session_state.first_name = email, new_name
                    st.rerun()
    st.stop()

# ניווט בסיסי בסרגל הצדי
with st.sidebar:
    st.write(f"היי {st.session_state.first_name}")
    mode = st.radio("תפריט", ["📚 האלבום שלי", "✨ סריקה"])
    if st.button("יציאה"):
        del st.session_state['user_email']
        st.rerun()

if mode == "✨ סריקה":
    st.header("סריקה חכמה")
    file = st.file_uploader("תמונה", type=["jpg", "png", "jpeg"])
    if file and st.button("שמור"):
        with st.status("מנתח..."):
            model = setup_ai(st.secrets["GEMINI_API_KEY"])
            res = model.generate_content([RECIPE_PROMPT, PIL.Image.open(file)])
            save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, res.text.split('\n')[0], res.text, "כללי")
            st.success("נשמר!")
            st.balloons()
else:
    # --- מצב אלבום: Swiper.js ---
    df = load_recipes_from_cloud(st.session_state.user_email)
    
    if df.empty:
        st.info("הספר ריק.")
    else:
        # בונים את כל הדפים כטקסט אחד ארוך של HTML
        slides_html = f"""
        <div class="swiper-slide">
            <div class="book-cover">
                <h1 style="color:white; font-family: serif;">{st.session_state.first_name}</h1>
                <p>ספר המתכונים הדיגיטלי</p>
                <p style="margin-top:50px; font-size:20px;">⬅️ החליקי שמאלה</p>
            </div>
        </div>
        """
        
        for _, row in df.iterrows():
            slides_html += f"""
            <div class="swiper-slide">
                <div class="recipe-page">
                    <h2 style="font-family: serif; border-bottom: 1px solid #eee;">{row['name']}</h2>
                    <p style="color: #BC8F8F; font-size: 12px;">{row.get('date', '')}</p>
                    <div style="white-space: pre-line;">{row['content']}</div>
                </div>
            </div>
            """

        # הזרקת ה-Swiper לתוך הדף
        full_swiper_code = f"""
        <div class="swiper mySwiper">
            <div class="swiper-wrapper">
                {slides_html}
            </div>
            <div class="swiper-pagination"></div>
        </div>

        <script>
          const swiper = new Swiper('.mySwiper', {{
            effect: 'cards',
            grabCursor: true,
            pagination: {{ el: ".swiper-pagination", clickable: true }},
          }});
        </script>
        """
        st.components.v1.html(full_swiper_code, height=700)
