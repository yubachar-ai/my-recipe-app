import streamlit as st
import PIL.Image
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, RECIPE_PROMPT

def show_add_recipe():
    st.markdown("### ✨ הוספת מתכון חדש")
    file = st.file_uploader("צלמי או העלי תמונה", type=["jpg", "png", "jpeg"])
    if file and st.button("שמירה לספר"):
        with st.status("ה-AI מנתח ושומר..."):
            model = setup_ai(st.secrets["GEMINI_API_KEY"])
            res = model.generate_content([RECIPE_PROMPT, PIL.Image.open(file)])
            save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, res.text.split('\n')[0], res.text, "כללי")
            st.success("נשמר!")
            st.balloons()

def show_my_book():
    st.markdown(f"### 📚 הספר של {st.session_state.first_name}")
    df = load_recipes_from_cloud(st.session_state.user_email)
    if df.empty:
        st.info("הספר ריק.")
    else:
        for _, row in df.iterrows():
            with st.expander(f"📖 {row['name']}"):
                st.markdown(f'<div class="recipe-card"><div style="white-space: pre-line;">{row["content"]}</div></div>', unsafe_allow_html=True)
