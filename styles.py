import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    /* ייבוא פונטים יוקרתיים בעברית */
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&family=Heebo:wght@300;500;800&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');

    /* הגדרות כלליות ויישור לימין */
    .stApp {
        background-color: #F9F7F2;
        direction: rtl;
        text-align: right;
    }

    /* שינוי פונט לכל האפליקציה - להתראות אריאל */
    html, body, [class*="st-"] {
        font-family: 'Assistant', sans-serif !important;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #2D2926 !important;
    }

    /* כרטיסיית מתכון בסגנון מגזין */
    .recipe-card {
        background-color: white;
        padding: 40px;
        border-radius: 4px;
        border-right: 6px solid #556B2F;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        line-height: 1.8;
        direction: rtl;
        text-align: right;
        font-size: 18px;
    }

    /* עיצוב תמונות */
    .hero-img {
        width: 100%;
        border-radius: 12px;
        object-fit: cover;
        height: 300px;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }

    /* יישור ספציפי לתיבות טקסט של סטרימליט */
    input, textarea {
        direction: rtl !important;
        text-align: right !important;
    }

    /* עיצוב כפתורים */
    .stButton>button {
        width: 100%;
        background-color: #556B2F !important;
        color: white !important;
        border-radius: 0px !important;
        border: none !important;
        padding: 15px !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
    }
    
    /* סידור ה-Sidebar */
    section[data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)
