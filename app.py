import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, RECIPE_PROMPT

# הגדרות עמוד
st.set_page_config(page_title="RecipeAI", page_icon="👩‍🍳", layout="wide")
apply_styles()

# 1. מסך כניסה לפי אימייל (מזהה ייחודי)
if 'user_email' not in st.session_state:
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🍎 RecipeAI Kitchen</h1>", unsafe_allow_html=True)
    
    col_login1, col_login2 = st.columns(2)
    with col_login1:
        first_name = st.text_input("איך קוראים לך?", placeholder="שם פרטי")
    with col_login2:
        email = st.text_input("כתובת אימייל:", placeholder="email@example.com")
        
    if st.button("כניסה למטבח האישי שלי 👩‍🍳"):
        if first_name and "@" in email:
            st.session_state.user_email = email.lower().strip()
            st.session_state.first_name = first_name
            st.rerun()
    st.stop()
    
# 2. שליפת נתונים מהכספת ואתחול המוח
current_user = st.session_state.user_email
api_key = st.secrets["GEMINI_API_KEY"]
model = setup_ai(api_key.strip())

# 3. ממשק האפליקציה
st.markdown(f"<h1 style='text-align: right;'>👩‍🍳 ספר המתכונים של {current_user.split('@')[0]}</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✨ סריקה חכמה", "📚 הספר שלי"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("📸 העלאת תמונה", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            img = PIL.Image.open(uploaded_file)
            # כיווץ תמונה כדי שירוץ מהר בטלפון
            if img.width > 800:
                ratio = 800 / img.width
                img = img.resize((800, int(img.height * ratio)), PIL.Image.LANCZOS)
            st.image(img, use_container_width=True)
    
    with col2:
        category = st.selectbox("קטגוריה:", ["🥗 סלטים", "🍰 קינוחים", "🍝 עיקריות", "🥐 מאפים", "🍲 מרקים"])
        if uploaded_file and st.button('שמור לספר ✨'):
            with st.status("מנתח ושומר...", expanded=False) as status:
                try:
                    response = model.generate_content([RECIPE_PROMPT, img])
                    full_text = response.text
                    recipe_name = full_text.split('\n')[0].replace('#', '').strip()
                    
                    # שמירה לענן (בגרסה זו - לקובץ CSV בשרת)
                    save_recipe_to_cloud(current_user, recipe_name, full_text, category)
                    
                    status.update(label="נשמר בהצלחה!", state="complete")
                    st.balloons()
                    st.markdown(f"<div class='recipe-card'>{full_text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"שגיאה בניתוח המתכון: {e}")

with tab2:
    st.markdown("### 📚 המתכונים שלי")
    df = load_recipes_from_cloud(current_user)
    if df is not None and not df.empty:
        search = st.text_input("🔍 חפשי מתכון...")
        if search:
            df = df[df['name'].str.contains(search, case=False) | df['content'].str.contains(search, case=False)]
        
        for i, row in df.iterrows():
            with st.expander(f"📖 {row['name']} | {row['category']}"):
                st.markdown(f"<div class='recipe-card'>{row['content']}</div>", unsafe_allow_html=True)
    else:
        st.info("הספר שלך עדיין ריק. סרקי מתכון כדי להתחיל!")
