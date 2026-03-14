import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    
    .stApp { background-color: #F9F7F2; direction: rtl; }
    [data-testid="stSidebarNav"], [data-testid="stHeader"], footer { display: none !important; }

    /* בר עליון */
    .main-header {
        background-color: white; padding: 15px; text-align: center;
        border-bottom: 1px solid #E8E4D8; position: fixed;
        top: 0; left: 0; right: 0; z-index: 1000;
    }
    
    .block-container { padding-top: 80px !important; max-width: 600px !important; margin: 0 auto; }

    /* כרטיסיית מתכון */
    .recipe-card {
        background: white; padding: 25px; border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-right: 6px solid #556B2F; text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)
