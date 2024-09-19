import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Set up the page layout and title
st.set_page_config(page_title="Google Sheets Search", layout="wide")

# Authenticate and connect to Google Sheets
def authenticate_google_sheets():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    client = gspread.authorize(credentials)
    return client

# Fetch data from Google Sheets and convert it to a DataFrame
def fetch_data(sheet_url):
    client = authenticate_google_sheets()
    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Format phone number with a leading zero if needed
def format_phone_number(phone_number):
    phone_str = str(phone_number)
    return '0' + phone_str if len(phone_str) == 9 else phone_str

# Google Sheets URL
sheet_url = "https://docs.google.com/spreadsheets/d/1bN11ozHCvrT2H-qPacU0-5uSCJW_HxVnpQyLsA88kqM/edit?usp=sharing"

# Fetch and display data
df = fetch_data(sheet_url)
search_term = st.text_input("ค้นหา (Search)")

# Apply custom CSS for left-aligned content
st.markdown("""
    <style>
    .container { width: 100%; }
    .left-content { width: 100%; text-align: left; }
    img { margin-bottom: 20px; }
    hr { border: none; border-top: 1px solid #ccc; margin: 30px 0; } /* Custom styling for horizontal rule */
    </style>
""", unsafe_allow_html=True)

# Filter and display search results
if search_term:
    search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    if not search_results.empty:
        for _, contact in search_results.iterrows():
            phone_number = format_phone_number(contact['โทรศัพท์'])
            st.markdown(f"""
                <div class="left-content">
                    <img src="{contact['ภาพ']}" width="150">
                    <h3>{contact['ยศ ชื่อ สกุล']}</h3>
                    <p><strong>ชื่อเล่น:</strong> {contact['ชื่อเล่น']}</p>
                    <p><strong>รุ่น:</strong> {contact['รุ่น']}</p>
                    <p><strong>ตำแหน่ง:</strong> {contact['ตำแหน่ง']}</p>
                    <p><strong>วัน เดือน ปี เกิด:</strong> {contact['วัน เดือน ปี เกิด']}</p>
                    <p><strong>หมายเลขโทรศัพท์:</strong> {phone_number}</p>
                </div>
                <hr> <!-- Add a horizontal line to separate each person -->
            """, unsafe_allow_html=True)
    else:
        st.write("ไม่พบข้อมูลที่ต้องการ (No matching data found)")
