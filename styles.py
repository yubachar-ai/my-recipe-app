import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    /* פונט Assistant מגוגל */
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;600&display=swap');

    /* רקע האפליקציה - צבע שמנת עדין */
    .stApp {
        background-color: #fdfaf5;
        font-family: 'Assistant', sans-serif;
    }

    /* עיצוב כרטיסיית המתכון */
    .recipe-card {
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border-right: 8px solid #FF4B4B;
        direction: rtl;
        text-align: right;
        white-space: pre-line;
        font-size: 18px;
        line-height: 1.7;
    }

    /* עיצוב הסרגל הצדי */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-left: 1px solid #e0e0e0;
    }
    
    /* כותרות */
    h1, h2, h3 {
        color: #2e3b4e;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)
