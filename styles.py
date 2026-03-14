import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Assistant:wght@300;400;600&display=swap');

    .stApp { background-color: #F9F7F2; }
    
    /* הסתרת אלמנטים מיותרים */
    header, footer {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}

    /* כריכת הספר */
    .book-cover {
        background-color: #556B2F;
        color: white;
        padding: 80px 40px;
        border-radius: 5px 15px 15px 5px;
        box-shadow: 15px 15px 30px rgba(0,0,0,0.2);
        text-align: center;
        margin: 40px auto;
        max-width: 350px;
        border-left: 10px solid #3e4f22;
        animation: fadeIn 0.8s ease-out;
    }

    /* דף המתכון */
    .recipe-page {
        background: white;
        padding: 40px;
        max-width: 500px;
        margin: 20px auto;
        min-height: 650px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border-radius: 2px;
        direction: rtl;
        text-align: right;
        font-family: 'Assistant', sans-serif;
        animation: pageSlide 0.4s ease-out;
    }

    @keyframes pageSlide {
        from { transform: translateX(30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* הוראות החלקה למשתמש */
    .swipe-hint {
        text-align: center;
        color: #BC8F8F;
        font-size: 14px;
        margin-top: 10px;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)
