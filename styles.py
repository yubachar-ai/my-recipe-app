import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Assistant:wght@300;400;600&display=swap');

    /* 1. הגדרות רוחב וניקוי בסיסי */
    .stApp { 
        background-color: #F9F7F2; 
        direction: rtl; 
    }

    /* מחיקה אגרסיבית של הניווט האוטומטי שתקוע לך באמצע */
    [data-testid="stSidebarNav"], [data-testid="stHeader"], footer, .stDeployButton {
        display: none !important;
    }

    /* 2. תיקון הרוחב של התוכן - שלא יהיה "חור" לבן באמצע המסך */
    .block-container {
        padding-top: 100px !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
        margin: 0 auto;
    }

    /* 3. בר עליון - עיצוב קומפקטי יותר */
    .main-header {
        background-color: #FFFFFF;
        padding: 15px 10px;
        text-align: center;
        border-bottom: 2px solid #8B0000;
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 9999;
        height: 70px;
    }
    
    .header-title {
        font-family: 'Playfair Display', serif;
        color: #8B0000;
        margin: 0;
        font-size: 20px;
        line-height: 1.2;
    }

    /* 4. עיצוב כרטיסיות המתכונים (Expanders) */
    .stExpander {
        border: 1px solid #E8E4D8 !important;
        background-color: white !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        overflow: hidden;
    }

    /* 5. תיקון ה-Sidebar */
    [data-testid="stSidebar"] {
        background-color: white !important;
        width: 280px !important;
    }

    /* ===== הזזה לימין ===== */

    /* מזיז את הסיידבר לימין */
    section[data-testid="stSidebar"]{
        right:0;
        left:auto;
    }

    /* מזיז את כפתור ה-3 פסים לימין */
    button[kind="header"]{
        right:1rem;
        left:auto;
    }

    /* שומר שהתוכן לא יברח */
    .css-18e3th9{
        padding-right:1rem;
    }

    /* ביטול מרווחים מיותרים בטלפון */
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }

    </style>
    """, unsafe_allow_html=True)
