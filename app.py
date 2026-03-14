import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, RECIPE_PROMPT

st.set_page_config(page_title="RecipeAI", page_icon="👩‍🍳", layout="wide")
apply_styles()

# מסך כניסה
if 'user_name' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>ברוכה הבאה ל-RecipeAI</h1>", unsafe_allow_html=True)
    name = st.text_input("איך קוראים לך?", placeholder="הקלידי שם...")
    if st.button("כניסה לספר המתכונים שלי"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.stop()

current_user = st.session_state.user_name
model = setup_ai("AIzaSyDs99bJ-UUG1jLT7lSaitXl6x4x23ZMDqQ")

st.markdown(f"<h1>👩‍🍳 ספר המתכונים של {current_user}</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✨ סריקה חכמה", "📚 הספר שלי"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("📸 העלאת תמונה", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            img = PIL.Image.open(uploaded_file)
            st.image(img, use_container_width=True)
    
    with col2:
        category = st.selectbox("קטגוריה:", ["🥗 סלטים", "🍰 קינוחים", "🍝 עיקריות", "🥐 מאפים", "🍲 מרקים"])
        if uploaded_file and st.button('שמור לספר ✨'):
            with st.status("מנתח ושומר בענן...", expanded=False) as status:
                response = model.generate_content([RECIPE_PROMPT, img])
                full_text = response.text
                recipe_name = full_text.split('\n')[0].replace('#', '').strip()
                save_recipe_to_cloud(current_user, recipe_name, full_text, category)
                status.update(label="נשמר בהצלחה!", state="complete")
            st.balloons()
            st.markdown(f"<div class='recipe-card'>{full_text}</div>", unsafe_allow_html=True)

with tab2:
    df = load_recipes_from_cloud(current_user)
    if df is not None and not df.empty:
        search = st.text_input("🔍 חפשי מתכון...")
        if search:
            df = df[df['name'].str.contains(search) | df['content'].str.contains(search)]
        
        for i, row in df.iterrows():
            with st.expander(f"📖 {row['name']} | {row['category']}"):
                st.markdown(f"<div class='recipe-card'>{row['content']}</div>", unsafe_allow_html=True)
    else:
        st.info(f"היי {current_user}, הספר שלך עדיין ריק.")
