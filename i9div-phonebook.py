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

# Streamlit layout for displaying contacts
st.title("Contact List")

# Search input
search_term = st.text_input("Enter contact name to search (leave blank to show all)")

# Filter contacts by search term or show all if blank
if search_term:
    search_results = [contact for contact in contacts if search_term.lower() in contact['ยศ ชื่อ สกุล'].lower()]
else:
    search_results = contacts

# Display contacts in a frame
if search_results:
    for contact in search_results:
        st.markdown(f"""
        <div style="border: 2px solid #d4d4d4; padding: 15px; margin-bottom: 15px;">
            <div style="display: flex;">
                <div style="flex: 1;">
                    <img src="{contact['ภาพ']}" alt="Contact Image" width="150">
                </div>
                <div style="flex: 2; padding-left: 20px;">
                    <div style='font-size:20px; line-height:2'>
                        <strong>รุ่น:</strong> {contact['รุ่น']}<br>
                        <strong>ยศ-ชื่อ:</strong> {contact['ยศ ชื่อ สกุล']}<br>
                        <strong>ชื่อเล่น:</strong> {contact['ชื่อเล่น']}<br>
                        <strong>ตำแหน่ง:</strong> {contact['ตำแหน่ง']}<br>
                        <strong>โทรศัพท์:</strong> {str(contact['โทรศัพท์'])}<br>
                        <strong>วัน เดือน ปี เกิด:</strong> {contact['วัน เดือน ปี เกิด']}<br>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("No contact found.")
