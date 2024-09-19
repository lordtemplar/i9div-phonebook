import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from st_copy_to_clipboard import st_copy_to_clipboard

# Set page title
st.set_page_config(page_title="ทำเนียบนายทหาร จปร. ค่ายสุรสีห์")

# Authenticate and connect to Google Sheets
@st.cache_resource
def authenticate_google_sheets():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
    )
    client = gspread.authorize(credentials)
    return client

# Fetch contact data from Google Sheets and store in session state to avoid repeated API calls
@st.cache_data
def fetch_contact_data(sheet_url):
    client = authenticate_google_sheets()
    sheet = client.open_by_url(sheet_url).sheet1  # Access the first sheet
    data = sheet.get_all_records()  # Fetch all records
    return pd.DataFrame(data)  # Convert data to DataFrame

# URL for the Google Sheets containing contact data
sheet_url = "https://docs.google.com/spreadsheets/d/1bN11ozHCvrT2H-qPacU0-5uSCJW_HxVnpQyLsA88kqM/edit?usp=sharing"

# Load the contact data
contacts_df = fetch_contact_data(sheet_url)

# Ensure phone number has a leading zero if required
def format_phone_number(phone_number):
    phone_number_str = str(phone_number)
    return '0' + phone_number_str if len(phone_number_str) == 9 else phone_number_str

# Function to display contact details
def display_contact_info(contact):
    phone_number = format_phone_number(contact['โทรศัพท์'])
    
    # Center content
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])  # Center alignment
        with col2:
            st.image(contact['ภาพ'], width=150)  # Display contact image
            
            # Display contact details
            st.write(f"**ยศ-ชื่อ**: {contact['ยศ ชื่อ สกุล']}")
            st.write(f"**ชื่อเล่น**: {contact['ชื่อเล่น']}")
            st.write(f"**รุ่น**: {contact['รุ่น']}")
            st.write(f"**ตำแหน่ง**: {contact['ตำแหน่ง']}")
            st.write(f"**วัน เดือน ปี เกิด**: {contact['วัน เดือน ปี เกิด']}")
            st.write(f"**โทรศัพท์**: {phone_number}")
            
            # Add Copy to Clipboard button
            st_copy_to_clipboard(phone_number)

# Streamlit layout for displaying contacts
st.title("ทำเนียบนายทหาร จปร. ค่ายสุรสีห์")

# Search inputs
name_search = st.text_input("ค้นหาด้วยชื่อ")
unit_search = st.text_input("ค้นหาด้วยหน่วย")
rank_search = st.text_input("ค้นหาด้วยยศ")

# Search button
if st.button("ค้นหา"):
    # Filter contacts based on user input
    search_results = contacts_df[
        (contacts_df['ยศ ชื่อ สกุล'].str.contains(name_search, case=False, na=False)) |
        (contacts_df['ชื่อเล่น'].str.contains(name_search, case=False, na=False))
    ]
    
    # Additional filtering if unit or rank search is provided
    if unit_search:
        search_results = search_results[search_results['ตำแหน่ง'].str.contains(unit_search, case=False, na=False)]
    if rank_search:
        search_results = search_results[search_results['ยศ ชื่อ สกุล'].str.contains(rank_search, case=False, na=False)]
    
    # Display results or show a warning if no results found
    if not search_results.empty:
        for _, contact in search_results.iterrows():
            display_contact_info(contact)
            st.write("---")  # Separator between results
    else:
        st.warning("ไม่พบข้อมูลที่ต้องการค้นหา")

