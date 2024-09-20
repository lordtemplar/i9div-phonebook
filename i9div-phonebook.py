import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Set page config first (before any other Streamlit elements)
st.set_page_config(
    page_title="ทำเนียบนายทหาร จปร. ค่ายสุรสีห์",  # Browser title
    layout="wide",  # Use wide layout
)

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

# Apply dark theme with custom CSS
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stTextInput, .stButton, .stSelectbox, .stMarkdown {
        background-color: #262730;
        color: #fafafa;
    }
    .stButton>button {
        background-color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Display the logo and title
st.markdown("""
    <div style="text-align:center;">
        <img src="https://firebasestorage.googleapis.com/v0/b/i9div-phonebook.appspot.com/o/logo.gif?alt=media&token=07073796-bd55-48ff-affa-eb82fdf59b7a" width="250"> <!-- Increased logo size -->
        <h5 style="color: #f1f1f1;">ทำเนียบนายทหาร จปร. ค่ายสุรสีห์</h5> <!-- Smaller text size -->
    </div>
""", unsafe_allow_html=True)

# Update search box label
search_term = st.text_input("ค้นหา (ยศ, ชื่อ, นามสกุล, รุ่น, ตำแหน่ง, สังกัด, ชั้นยศ, หมายเลขโทรศัพท์)")

# Filter and display search results
if search_term:
    search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    if not search_results.empty:
        for _, contact in search_results.iterrows():
            phone_number = format_phone_number(contact['โทรศัพท์'])
            st.markdown(f"""
                <div class="left-content">
                    <img src="{contact['ภาพ']}" width="200"> <!-- Image reduced to 200px and centered -->
                    <h3 class="centered-text">{contact['ยศ ชื่อ สกุล']}</h3> <!-- Centered name -->
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
