import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_csv, load_recipes, RECIPE_PROMPT

# הגדרות עמוד
st.set_page_config(page_title="RecipeAI", page_icon="👩‍🍳", layout="wide")
apply_styles()

# אתחול המוח
model = setup_ai("הדביקי_כאן_את_המפתח_שלך")

st.markdown("<h1>👩‍🍳 ספר המתכונים הדיגיטלי</h1>", unsafe_allow_html=True)

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
            with st.status("מנתח...", expanded=False) as status:
                response = model.generate_content([RECIPE_PROMPT, img])
                full_text = response.text
                recipe_name = full_text.split('\n')[0].replace('#', '').strip()
                save_recipe_to_csv(recipe_name, full_text, category)
                status.update(label="נשמר!", state="complete")
            st.balloons()
            st.markdown(f"<div class='recipe-card'>{full_text}</div>", unsafe_allow_html=True)

with tab2:
    df = load_recipes()
    if df is not None:
        search = st.text_input("🔍 חפשי מתכון...")
        if search:
            df = df[df['שם'].str.contains(search) | df['תוכן'].str.contains(search)]
        
        for i, row in df.iterrows():
            with st.expander(f"📖 {row['שם']} | {row['קטגוריה']}"):
                st.markdown(f"<div class='recipe-card'>{row['תוכן']}</div>", unsafe_allow_html=True)
    else:
        st.info("הספר ריק עדיין.")