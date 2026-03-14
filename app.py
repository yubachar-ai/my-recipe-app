import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, get_user_from_db, RECIPE_PROMPT

# חייב להיות בשורה הראשונה
st.set_page_config(page_title="RecipeAI", layout="wide", initial_sidebar_state="collapsed")
apply_styles()

# (כאן הקוד של ה-Auth/כניסה שלך...)

# בר עליון קבוע
st.markdown(f'<div class="main-header"><h1 style="font-family:serif; font-size:22px;">ספר המתכונים של {st.session_state.get("first_name", "יובל")}</h1></div>', unsafe_allow_html=True)

# תפריט ה-3 פסים (Sidebar)
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("ניווט")
    # כאן אנחנו יוצרים את התפריט היחיד באפליקציה
    mode = st.radio("לאן לעבור?", ["📚 כניסה לספר", "✨ הוספת מתכון"], label_visibility="collapsed")
    st.markdown("---")
    if st.button("יציאה מהחשבון"):
        del st.session_state['user_email']
        st.rerun()

# הצגת התוכן לפי הבחירה בתפריט
if mode == "✨ הוספת מתכון":
    st.markdown("### ✨ הוספת מתכון")
    # ... (קוד ההעלאה שלך)
else:
    st.markdown("### 📚 המתכונים שלי")
    # ... (קוד הצגת המתכונים שלך)
