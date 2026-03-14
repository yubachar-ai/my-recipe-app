import streamlit as st
import PIL.Image
import streamlit.components.v1 as components
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, get_user_from_db, RECIPE_PROMPT

# הגדרות עמוד
st.set_page_config(page_title="RecipeAI", layout="wide")
apply_styles()

# ניהול עמודים דרך ה-URL (בשביל ה-Swipe)
params = st.query_params
if "p" in params:
    st.session_state.page_index = int(params["p"])

if 'page_index' not in st.session_state:
    st.session_state.page_index = 0

# ניהול כניסה
if 'user_email' not in st.session_state:
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>RecipeAI</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email = st.text_input("אימייל לכניסה:", placeholder="email@example.com")
        if email:
            name = get_user_from_db(email)
            if name:
                if st.button(f"כניסה לאלבום של {name}"):
                    st.session_state.user_email = email.lower().strip()
                    st.session_state.first_name = name
                    st.rerun()
            else:
                new_name = st.text_input("איך קוראים לך?")
                if st.button("יצירת אלבום"):
                    if new_name:
                        st.session_state.user_email = email.lower().strip()
                        st.session_state.first_name = new_name
                        st.rerun()
    st.stop()

# ניווט צדי
with st.sidebar:
    st.markdown(f"### שלום {st.session_state.first_name}")
    mode = st.radio("תפריט:", ["📚 האלבום שלי", "✨ סריקה"])
    if st.button("יציאה"):
        del st.session_state['user_email']
        st.rerun()

# לוגיקה
if mode == "✨ סריקה":
    st.header("סריקה חכמה")
    file = st.file_uploader("תמונה", type=["jpg", "png", "jpeg"])
    if file and st.button("שמור"):
        model = setup_ai(st.secrets["GEMINI_API_KEY"])
        img = PIL.Image.open(file)
        res = model.generate_content([RECIPE_PROMPT, img])
        save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, res.text.split('\n')[0], res.text, "כללי")
        st.balloons()

else:
    df = load_recipes_from_cloud(st.session_state.user_email)
    if not df.empty:
        total_pages = len(df) + 1
        curr = st.session_state.page_index

        # תצוגת דף
        if curr == 0:
            st.markdown(f"<div class='book-cover'><h1>{st.session_state.first_name}</h1><p>החליקי לדפדוף</p></div>", unsafe_allow_html=True)
        else:
            recipe = df.iloc[curr - 1]
            st.markdown(f"<div class='recipe-page'><h2>{recipe['name']}</h2><hr>{recipe['content']}</div>", unsafe_allow_html=True)

        # הזרקת ה-JS ל-Swipe (גרסת 2026 שעובדת!)
        swipe_html = f"""
        <script>
        var startX;
        var currPage = {curr};
        var totalPages = {total_pages};
        
        document.addEventListener('touchstart', function(e) {{ startX = e.touches[0].clientX; }}, false);
        document.addEventListener('touchend', function(e) {{
            var endX = e.changedTouches[0].clientX;
            var diffX = startX - endX;
            if (Math.abs(diffX) > 60) {{
                var newPage = currPage;
                if (diffX > 0 && currPage < totalPages - 1) newPage++;
                else if (diffX < 0 && currPage > 0) newPage--;
                
                if (newPage !== currPage) {{
                    const url = new URL(window.location);
                    url.searchParams.set('p', newPage);
                    window.parent.location.href = url.href;
                }}
            }}
        }}, false);
        </script>
        """
        components.html(swipe_html, height=0)
        
        # כפתורי גיבוי (למקרה שהחלקה לא עובדת במכשיר ספציפי)
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,2,1])
        with c1:
            if curr > 0:
                if st.button("➡️"): st.query_params["p"] = str(curr - 1)
        with c2:
            st.markdown(f"<p style='text-align:center;'>{curr + 1} / {total_pages}</p>", unsafe_allow_html=True)
        with c3:
            if curr < total_pages - 1:
                if st.button("⬅️"): st.query_params["p"] = str(curr + 1)
