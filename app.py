import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, RECIPE_PROMPT

st.set_page_config(page_title="RecipeAI", page_icon="👩‍🍳", layout="wide")
apply_styles()

# מסך כניסה
if 'user_email' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>ברוכה הבאה ל-RecipeAI</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fname = st.text_input("איך קוראים לך?", placeholder="שם פרטי")
    with col2:
        email = st.text_input("אימייל (לשמירת המתכונים):", placeholder="email@example.com")
    
    if st.button("כניסה לספר שלי"):
        if fname and "@" in email:
            st.session_state.user_email = email.lower().strip()
            st.session_state.first_name = fname
            st.rerun()
    st.stop()

# אתחול
api_key = st.secrets["GEMINI_API_KEY"]
model = setup_ai(api_key.strip())

# סרגל צדי (Sidebar) - ה"אלבום"
with st.sidebar:
    st.title(f"היי {st.session_state.first_name}! 👋")
    mode = st.radio("לאן הולכים?", ["📚 דפדוף באלבום", "✨ סריקת מתכון חדש"])
    st.markdown("---")
    if mode == "📚 דפדוף באלבום":
        st.subheader("סינון קטגוריה:")
        cat_filter = st.selectbox("בחר:", ["הכל", "🥗 סלטים", "🍰 קינוחים", "🍝 עיקריות", "🥐 מאפים", "🍲 מרקים"])

# מצב סריקה
if mode == "✨ סריקת מתכון חדש":
    st.header("סריקת מתכון חדש")
    uploaded_file = st.file_uploader("צלמי או העלי תמונה", type=["jpg", "png", "jpeg"])
    category = st.selectbox("לאיזו קטגוריה זה שייך?", ["🥗 סלטים", "🍰 קינוחים", "🍝 עיקריות", "🥐 מאפים", "🍲 מרקים"])
    
    if uploaded_file and st.button("שמור לאלבום ✨"):
        with st.status("מנתח ושומר...") as status:
            img = PIL.Image.open(uploaded_file)
            response = model.generate_content([RECIPE_PROMPT, img])
            recipe_name = response.text.split('\n')[0].replace('#','').strip()
            save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, recipe_name, response.text, category)
            status.update(label="נשמר באלבום!", state="complete")
            st.balloons()

# מצב אלבום
else:
    st.header(f"האלבום של {st.session_state.first_name}")
    df = load_recipes_from_cloud(st.session_state.user_email)
    
    if not df.empty:
        if cat_filter != "הכל":
            df = df[df['category'] == cat_filter]
        
        for i, row in df.iterrows():
            with st.expander(f"📖 {row['name']} ({row.get('date', '')})"):
                st.markdown(f"<div class='recipe-card'>{row['content']}</div>", unsafe_allow_html=True)
    else:
        st.info("האלבום עדיין ריק. לכי לסריקה!")
