import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    /* ייבוא גופנים יוקרתיים */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;600&display=swap');

    /* הגדרות בסיס - Olive & Linen Palette */
    :root {
        --bg-color: #F9F7F2;
        --card-bg: #FFFFFF;
        --olive: #556B2F;
        --rosy: #BC8F8F;
        --charcoal: #2D2926;
    }

    .stApp {
        background-color: var(--bg-color);
        color: var(--charcoal);
        font-family: 'Inter', sans-serif;
    }

    /* כותרות Serif יוקרתיות */
    h1, h2, h3, .serif-font {
        font-family: 'Playfair Display', serif !important;
        color: var(--charcoal) !important;
        font-weight: 700 !important;
    }

    /* כרטיסיות ה-Dashboard (Main Actions) */
    .dashboard-card {
        background-color: var(--card-bg);
        border: 1px solid rgba(85, 107, 47, 0.1);
        border-radius: 12px;
        padding: 40px 20px;
        text-align: center;
        transition: all 0.4s ease;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }

    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(85, 107, 47, 0.08);
        border-color: var(--olive);
    }

    .dashboard-icon {
        font-size: 40px;
        margin-bottom: 15px;
        color: var(--olive);
    }

    /* עיצוב ה"ספר הדיגיטלי" (The Digital Book View) */
    .recipe-page {
        background-color: var(--card-bg);
        padding: 50px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin: 20px auto;
        max-width: 800px;
        border-right: 1px solid #eee;
        line-height: 1.8;
        position: relative;
        animation: fadeIn 0.8s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* סרגל צדי (Sidebar) בסגנון נקי */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-left: 1px solid #E8E4D8;
    }

    /* כפתורים בסגנון Olive */
    .stButton>button {
        background-color: var(--olive) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 25px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border: none !important;
        transition: 0.3s !important;
    }

    .stButton>button:hover {
        background-color: #3e4f22 !important;
        box-shadow: 0 4px 12px rgba(85, 107, 47, 0.3) !important;
    }

    /* עיצוב התפריט (Radio Buttons) */
    div[data-row-metadata] {
        background: transparent !important;
    }
    
    /* הסרת אלמנטים מיותרים של סטרימליט למראה נקי */
    #MainMenu, footer, header {display: none !important;}
    </style>
    """, unsafe_allow_html=True)
