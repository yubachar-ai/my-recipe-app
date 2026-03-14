import google.generativeai as genai
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- הגדרות AI ---
def setup_ai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('models/gemini-3-flash-preview')

RECIPE_PROMPT = "חלץ שם מתכון (שורה ראשונה), מצרכים והוראות בעברית. בלי הקדמות."

# --- פונקציות בסיס הנתונים ---

def get_user_from_db(email):
    """בודק אם המשתמש כבר קיים בגיליון ושולף את השם שלו"""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        if df is not None and not df.empty:
            df.columns = [c.strip().lower() for c in df.columns]
            user_row = df[df['user'].astype(str).str.lower() == email.lower().strip()]
            if not user_row.empty:
                return user_row.iloc[0]['first_name']
    except Exception:
        pass
    return None

def save_recipe_to_cloud(user_email, first_name, name, content, category):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0)
    
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    new_data = pd.DataFrame({
        'user': [user_email.lower().strip()],
        'first_name': [first_name],
        'date': [current_date],
        'name': [name],
        'category': [category],
        'content': [content]
    })
    
    updated_df = pd.concat([df, new_data], ignore_index=True)
    conn.update(data=updated_df)

def load_recipes_from_cloud(user_email):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        if df is not None and not df.empty:
            df.columns = [c.strip().lower() for c in df.columns]
            return df[df['user'].astype(str).str.lower() == user_email.lower().strip()]
    except Exception:
        pass
    return pd.DataFrame()

# שורה חשובה כדי שקבצים אחרים יוכלו לייבא את המשתנה הזה
__all__ = ['setup_ai', 'get_user_from_db', 'save_recipe_to_cloud', 'load_recipes_from_cloud', 'RECIPE_PROMPT']
