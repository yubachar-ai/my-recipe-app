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
הנחיות: השורה הראשונה היא שם המתכון בלבד. אל תוסיף הקדמות.
"""

def get_connection():
    return st.connection("gsheets", type=GSheetsConnection)

def save_recipe_to_cloud(user_name, name, content, category):
    conn = get_connection()
    url = "כאן_הדביקי_את_הלינק_של_הגיליון_שלך"
    
    # קריאת הנתונים הקיימים
    try:
        df = conn.read(spreadsheet=url)
    except:
        df = pd.DataFrame(columns=['user', 'name', 'category', 'content'])
    
    # יצירת שורה חדשה
    new_data = pd.DataFrame({
        'user': [user_name],
        'name': [name],
        'category': [category],
        'content': [content]
    })
    
    updated_df = pd.concat([df, new_data], ignore_index=True)
    
    # שמירה חזרה לענן
    conn.update(spreadsheet=url, data=updated_df)

def load_recipes_from_cloud(user_name):
    conn = get_connection()
    url = "כאן_הדביקי_את_הלינק_של_הגיליון_שלך"
    try:
        df = conn.read(spreadsheet=url)
        return df[df['user'] == user_name]
    except:
        return pd.DataFrame()
