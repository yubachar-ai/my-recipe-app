import streamlit as st
import PIL.Image
from styles import apply_styles
from logic import setup_ai, save_recipe_to_cloud, load_recipes_from_cloud, get_user_from_db, RECIPE_PROMPT

st.set_page_config(page_title="RecipeAI", layout="wide")
apply_styles()

# (כאן מגיע קוד ה-Auth שלך - כניסה/הרשמה כרגיל)
# ... [הקוד של הכניסה נשאר ללא שינוי] ...

# סרגל צדי לניווט כללי
with st.sidebar:
    st.write(f"היי {st.session_state.get('first_name', 'אורחת')}")
    mode = st.radio("תפריט", ["📚 הספר שלי", "✨ סריקה חדשה"])

if mode == "✨ סריקה חדשה":
    st.header("סריקה חכמה")
    file = st.file_uploader("העלי תמונה", type=["jpg", "png", "jpeg"])
    if file and st.button("שמור"):
        with st.status("מנתח..."):
            model = setup_ai(st.secrets["GEMINI_API_KEY"])
            res = model.generate_content([RECIPE_PROMPT, PIL.Image.open(file)])
            save_recipe_to_cloud(st.session_state.user_email, st.session_state.first_name, res.text.split('\n')[0], res.text, "כללי")
            st.success("נשמר!")
            st.rerun()

else:
    # --- מצב ספר: ניווט לפי טאבים ---
    st.markdown(f"<h1 style='text-align: center;'>הספר של {st.session_state.get('first_name', '')}</h1>", unsafe_allow_html=True)
    
    df = load_recipes_from_cloud(st.session_state.user_email)
    
    if df.empty:
        st.info("הספר ריק.")
    else:
        # יצירת טאב לכל מתכון - זה הופך את זה לספר "מדופדף" לפי בחירה
        recipe_names = df['name'].tolist()
        tabs = st.tabs(recipe_names)
        
        for i, tab in enumerate(tabs):
            with tab:
                row = df.iloc[i]
                st.markdown(f"""
                    <div class="recipe-page">
                        <p style="color: #BC8F8F;">{row.get('date', '')}</p>
                        <h2 style="font-size: 38px;">{row['name']}</h2>
                        <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
                        <div style="white-space: pre-line; font-size: 18px; line-height: 2;">
                            {row['content']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
