import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Assistant:wght@300;400;600&display=swap');

    /* מחיקת תפריט הניווט האוטומטי שחונק את המסך */
    [data-testid="stSidebarNav"] {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    footer {display: none !important;}

    /* רקע ויישור לימין */
    .stApp { 
        background-color: #F9F7F2; 
        direction: rtl; 
    }

    /* הבר העליון הלבן */
    .main-header {
        background-color: #FFFFFF;
        padding: 20px;
        text-align: center;
        border-bottom: 1px solid #E8E4D8;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    
    .header-title {
        font-family: 'Playfair Display', serif;
        color: #2D2926;
        margin: 0;
        font-size: 22px;
    }

    /* תיקון מרווחים כדי שהתוכן לא ייחתך */
    .block-container {
        padding-top: 100px !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* עיצוב רשימת המתכונים */
    .stExpander {
        background-color: white !important;
        border: 1px solid #E8E4D8 !important;
        border-radius: 8px !important;
        margin-bottom: 10px !important;
    }

    .recipe-card {
        background: white;
        padding: 20px;
        text-align: right;
        direction: rtl;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)
