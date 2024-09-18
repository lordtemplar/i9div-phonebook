import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Authenticate using Streamlit Secrets
def authenticate_google_sheets():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    client = gspread.authorize(credentials)
    return client

# Fetch contact data from Google Sheets
def fetch_contact_data(sheet_url):
    client = authenticate_google_sheets()
    sheet = client.open_by_url(sheet_url).sheet1  # Access the first sheet
    contacts = sheet.get_all_records()  # Fetch all records from the sheet
    return contacts

# URL for the Google Sheets containing contact data
sheet_url = "https://docs.google.com/spreadsheets/d/1bN11ozHCvrT2H-qPacU0-5uSCJW_HxVnpQyLsA88kqM/edit?usp=sharing"

# Fetch the contact data from Google Sheets
contacts = fetch_contact_data(sheet_url)

# Streamlit layout for contact search and result display
st.title("Contact Search")

# Search input
search_term = st.text_input("Enter contact name to search")

# Filter contacts by search term
if search_term:
    search_results = [contact for contact in contacts if search_term.lower() in contact['name'].lower()]
    
    if search_results:
        # Display search results
        for contact in search_results:
            col1, col2 = st.columns([1, 2])
            with col1:
                # Display the contact's photo (assuming photo_url column contains the Google Drive direct link)
                st.image(contact["photo_url"], width=250)
            with col2:
                # Display contact details
                st.markdown(f"""
                <div style='font-size:20px; line-height:2'>
                <strong>รุ่น:</strong> {contact['rank']}<br>
                <strong>ยศ-ชื่อ:</strong> {contact['name']}<br>
                <strong>ตำแหน่ง:</strong> {contact['position']}<br>
                <strong>โทรศัพท์:</strong> {contact['phone']}<br>
                <strong>วัน เดือน ปี เกิด:</strong> {contact['birthdate']}<br>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.error("No contact found.")
