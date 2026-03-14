import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600&family=Playfair+Display:wght@700&display=swap');

    /* הגדרות בסיס */
    .stApp { 
        background-color: #F9F7F2; 
        direction: rtl; 
    }

    /* העלמת התפריט האוטומטי המציק */
    [data-testid="stSidebarNav"] {display: none !important;}
    
    /* עיצוב ה-Sidebar (שיהיה לבן ונקי) */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-left: 1px solid #E8E4D8;
        min-width: 250px !important;
    }

    /* עיצוב הבר העליון */
    .main-header {
        background-color: white;
        padding: 15px;
        text-align: center;
        border-bottom: 1px solid #E8E4D8;
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 1000;
    }

    /* תיקון המרווח של התוכן - שלא יימרח לאמצע */
    .block-container {
        padding-top: 80px !important;
        max-width: 600px !important; /* זה שומר על המתכונים במרכז נקי ולא מפוזר */
        margin: 0 auto;
    }

    /* עיצוב רשימת המתכונים (Expanders) */
    .stExpander {
        border: none !important;
        background-color: white !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)
