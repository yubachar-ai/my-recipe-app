import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, get_user_from_db, RECIPE_PROMPT

# הגדרות תצוגה יוקרתית
st.set_page_config(page_title="RecipeAI | Digital Heirloom", page_icon="👩‍🍳", layout="wide")
apply_styles()

# ניהול כניסה (Auth Screen)
if 'user_email' not in st.session_state:
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True) # מרווח עליון
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>RecipeAI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #BC8F8F; font-style: italic;'>Your Digital Heirloom Recipe Book</p>", unsafe_allow_html=True)
    
    # מרכז הכניסה
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        email_input = st.text_input("הזיני אימייל לכניסה למטבח:", placeholder="email@example.com")
        
        if email_input:
            existing_name = get_user_from_db(email_input)
            
            if existing_name:
                st.markdown(f"<p style='text-align: center;'>שמחים שחזרת, <b>{existing_name}</b></p>", unsafe_allow_html=True)
                if st.button(f"פתיחת האלבום של {existing_name}"):
                    st.session_state.user_email = email_input.lower().strip()
                    st.session_state.first_name = existing_name
                    st.session_state.current_page = "🏠 דף הבית" # דף ברירת מחדל
                    st.rerun()
            else:
                st.markdown("<p style='text-align: center; color: #556B2F;'>נראה שזו פעם ראשונה שלך! איך קוראים לך?</p>", unsafe_allow_html=True)
                new_name = st.text_input("שם פרטי:", placeholder="השם שלך...")
                if st.button("יצירת אלבום אישי"):
                    if new_name:
                        st.session_state.user_email = email_input.lower().strip()
                        st.session_state.first_name = new_name
                        st.session_state.current_page = "🏠 דף הבית"
                        st.rerun()
    st.stop()

# --- אתחול מודל AI ---
api_key = st.secrets["GEMINI_API_KEY"]
model = setup_ai(api_key.strip())

# --- סרגל צדי מינימליסטי ---
with st.sidebar:
    st.markdown(f"<h2 class='serif-font'>היי, {st.session_state.first_name}</h2>", unsafe_allow_html=True)
    page = st.radio("", ["🏠 דף הבית", "📚 האלבום שלי", "✨ סריקה חדשה"], key="nav_radio")
    
    st.markdown("<div style='height: 40vh;'></div>", unsafe_allow_html=True)
    if st.button("החלפת משתמש"):
        del st.session_state['user_email']
        st.rerun()

# --- תוכן האפליקציה (Main View) ---

# דף הבית (Main Dashboard)
if page == "🏠 דף הבית":
    st.markdown(f"<h1 style='text-align: center; margin-top: 30px;'>בוקר טוב, {st.session_state.first_name}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #BC8F8F; margin-bottom: 50px;'>מה נבשל היום?</p>", unsafe_allow_html=True)
    
    col_dash1, col_dash2 = st.columns(2)
    
    with col_dash1:
        st.markdown("""
            <div class='dashboard-card'>
                <div class='dashboard-icon'>📖</div>
                <h3 class='serif-font'>הספר הדיגיטלי</h3>
                <p>דפדוף במתכונים שנשמרו באהבה</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("לפתיחת הספר ➔"):
            st.info("בחרי ב-'האלבום שלי' בסרגל הצדי") # בסטרימליט זה הדרך הקלה לנווט

    with col_dash2:
        st.markdown("""
            <div class='dashboard-card'>
                <div class='dashboard-icon'>📸</div>
                <h3 class='serif-font'>סריקה חדשה</h3>
                <p>הפיכת מתכון נייר לנכס דיגיטלי</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("להתחלת סריקה ➔"):
            st.info("בחרי ב-'סריקה חדשה' בסרגל הצדי")

# דף סריקה (AI Recipe Uploader)
elif page == "✨ סריקה חדשה":
    st.markdown("<h2 class='serif-font'>הוספת מתכון לאלבום</h2>", unsafe_allow_html=True)
    
    col_up1, col_up2 = st.columns([1, 1])
    with col_up1:
        uploaded_file = st.file_uploader("גררי תמונה לכאן", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            img = PIL.Image.open(uploaded_file)
            st.image(img, use_container_width=True)
            
    with col_up2:
        category = st.selectbox("קטגוריה:", ["🥗 סלטים", "🍰 קינוחים", "🍝 עיקריות", "🥐 מאפים", "🍲 מרקים"])
        if uploaded_file and st.button("שמור לספר המשפחתי ✨"):
            with st.status("ה-AI סורק ומנתח את הכתב...", expanded=True) as status:
                response = model.generate_content([RECIPE_PROMPT, img])
                full_text = response.text
                recipe_name = full_text.split('\n')[0].replace('#','').strip()
                save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, recipe_name, full_text, category)
                status.update(label="נשמר בהצלחה!", state="complete")
                st.balloons()

# דף האלבום (The Digital Book View)
else:
    st.markdown(f"<h2 class='serif-font'>הספר הדיגיטלי של משפחת {st.session_state.first_name}</h2>", unsafe_allow_html=True)
    
    # סרגל חיפוש מינימליסטי
    search = st.text_input("🔍 חפשי מתכון...", placeholder="למשל: עוגת שוקולד")
    
    df = load_recipes_from_cloud(st.session_state.user_email)
    
    if not df.empty:
        if search:
            df = df[df['name'].str.contains(search, case=False, na=False)]
            
        for i, row in df.iterrows():
            with st.expander(f"📖 {row['name']} | {row.get('date', '')}"):
                # שימוש בפורמט Page של האלבום
                st.markdown(f"<div class='recipe-page'>{row['content']}</div>", unsafe_allow_html=True)
    else:
        st.info("הספר עדיין ריק. זמן למלא אותו בזיכרונות טעימים.")
