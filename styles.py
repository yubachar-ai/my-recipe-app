import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Assistant:wght@300;400;600&display=swap');

    /* צבעי בסיס - בז' יוקרתי */
    .stApp {
        background-color: #F9F7F2;
        color: #333333;
        direction: rtl;
    }

    /* כותרות - אדום יין עמוק */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #8B0000 !important;
        font-weight: 700;
        text-align: right;
    }

    /* כרטיסיית מתכון - נראית כמו דף בספר */
    .recipe-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-right: 6px solid #556B2F; /* נגיעה של ירוק זית */
        margin-bottom: 20px;
        text-align: right;
        font-family: 'Assistant', sans-serif;
    }

    /* עיצוב כפתורים - ירוק זית */
    .stButton>button {
        background-color: #556B2F !important;
        color: white !important;
        border-radius: 0px !important; /* מראה שטוח ומודרני */
        border: none !important;
        font-family: 'Assistant', sans-serif;
        font-weight: 600;
        letter-spacing: 1px;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #3e4f22 !important;
    }

    /* עיצוב תיבות טקסט */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #FFFFFF !important;
        border: 1px solid #E8E4D8 !important;
        color: #333333 !important;
    }

    /* הסתרת כפתורי סטרימליט מיותרים */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    </style>
    """, unsafe_allow_html=True)
