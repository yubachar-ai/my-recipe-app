import google.generativeai as genai
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# הגדרת ה-AI
def setup_ai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('models/gemini-3-flash-preview')

RECIPE_PROMPT = """
תפקיד: מחלץ נתונים מקצועי מתמונות מתכונים.
המשימה: חלץ את המידע מהתמונה והחזר אותו בעברית לפי הפורמט הבא בלבד.
הנחיות: השורה הראשונה היא שם המתכון בלבד. בלי הקדמות.
"""

def save_recipe_to_cloud(user_email, name, content, category):
    # יצירת חיבור באמצעות ה-Secrets שהגדרת
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # קריאת הנתונים הקיימים
    try:
        df = conn.read()
    except:
        # אם הגיליון ריק לגמרי, ניצור מבנה בסיסי
        df = pd.DataFrame(columns=['user', 'name', 'category', 'content'])
    
    # יצירת שורה חדשה בפורמט של טבלה
    new_data = pd.DataFrame({
        'user': [user_email],
        'name': [name],
        'category': [category],
        'content': [content]
    })
    
    # חיבור השורה החדשה (שימוש ב-concat במקום append)
    updated_df = pd.concat([df, new_data], ignore_index=True)
    
    # עדכון הגיליון בענן
    conn.update(data=updated_df)

def load_recipes_from_cloud(user_email):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        if df is not None and not df.empty:
            return df[df['user'] == user_email]
    except:
        pass
    return pd.DataFrame()
