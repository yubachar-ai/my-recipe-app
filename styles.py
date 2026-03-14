import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Assistant:wght@300;400;600&display=swap');

    /* רקע לינן יוקרתי */
    .stApp { 
        background-color: #F9F7F2; 
        direction: rtl; 
    }
    
    /* עיצוב הבר העליון הקבוע */
    .main-header {
        background-color: white;
        padding: 15px;
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
        font-size: 24px;
    }

    /* מרווח כדי שהתוכן לא יתחבא תחת הבר העליון */
    .content-area {
        margin-top: 80px;
    }

    /* עיצוב כרטיסיית מתכון */
    .recipe-card {
        background: white;
        padding: 30px;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-right: 6px solid #556B2F;
        margin-bottom: 20px;
        text-align: right;
    }

    /* עיצוב התפריט הצדי (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-left: 1px solid #E8E4D8;
    }
    
    h2, h3 { font-family: 'Playfair Display', serif; color: #2D2926; }
    </style>
    """, unsafe_allow_html=True)
