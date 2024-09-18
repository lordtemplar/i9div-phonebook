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

# Convert Google Drive link to direct image link
def convert_drive_url(drive_url):
    try:
        if drive_url:  # Check if the URL exists
            file_id = drive_url.split('/')[-2]  # Extract the file ID from the Google Drive link
            return f"https://drive.google.com/uc?export=view&id={file_id}"
        return None
    except IndexError:
        return None

# URL for the Google Sheets containing contact data
sheet_url = "https://docs.google.com/spreadsheets/d/1bN11ozHCvrT2H-qPacU0-5uSCJW_HxVnpQyLsA88kqM/edit?usp=sharing"

# Fetch the contact data from Google Sheets
contacts = fetch_contact_data(sheet_url)

# Streamlit layout for displaying all contacts
st.title("Contact List")

# Display all contacts
if contacts:
    for contact in contacts:
        col1, col2 = st.columns([1, 2])
        with col1:
            # Convert Google Drive link to direct image URL and display the contact's photo
            image_url = convert_drive_url(contact["ภาพ"])
            if image_url:
                st.image(image_url, width=250)
            else:
                st.error("Image not available or invalid link.")
                
        with col2:
            # Display contact details
            st.markdown(f"""
            <div style='font-size:20px; line-height:2'>
            <strong>รุ่น:</strong> {contact['รุ่น']}<br>
            <strong>ยศ-ชื่อ:</strong> {contact['ยศ ชื่อ สกุล']}<br>
            <strong>ชื่อเล่น:</strong> {contact['ชื่อเล่น']}<br>
            <strong>ตำแหน่ง:</strong> {contact['ตำแหน่ง']}<br>
            <strong>โทรศัพท์:</strong> {str(contact['โทรศัพท์'])}<br>
            <strong>วัน เดือน ปี เกิด:</strong> {contact['วัน เดือน ปี เกิด']}<br>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("No contact found.")
