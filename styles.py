import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Assistant:wght@300;400;600&display=swap');

    /* רקע לינן ויישור לימין */
    .stApp { 
        background-color: #F9F7F2; 
        direction: rtl; 
    }
    
    /* הסתרת כפתורי סטרימליט מיותרים והתפריט המובנה שצף */
    #MainMenu, footer, header {visibility: hidden !important;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0) !important;}

    /* הבר העליון הממותג שלנו */
    .main-header {
        background-color: #FFFFFF;
        padding: 20px;
        text-align: center;
        border-bottom: 1px solid #E8E4D8;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    
    .header-title {
        font-family: 'Playfair Display', serif;
        color: #2D2926;
        margin: 0;
        font-size: 22px;
    }

    /* מרווח לתוכן - למנוע מהכותרת להסתיר */
    .block-container {
        padding-top: 100px !important;
        max-width: 800px !important;
    }

    /* עיצוב כרטיסיית מתכון */
    .recipe-card {
        background: white;
        padding: 30px;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        border-right: 6px solid #556B2F;
        margin-bottom: 20px;
        text-align: right;
    }

    /* עיצוב ה-Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-left: 1px solid #E8E4D8;
    }
    
    /* הפיכת ה-Radio למשהו שנראה כמו תפריט יוקרתי */
    .stRadio > div {
        flex-direction: column !important;
        gap: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
