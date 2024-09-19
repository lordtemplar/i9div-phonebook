import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Set page title
st.set_page_config(page_title="ทำเนียบนายทหาร จปร. ค่ายสุรสีห์")

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

# Function to ensure the phone number is treated as a string with leading zeros
def format_phone_number(phone_number):
    return str(phone_number).zfill(10)  # Ensure phone number is always 10 digits long, padded with zeros

# URL for the Google Sheets containing contact data
sheet_url = "https://docs.google.com/spreadsheets/d/1bN11ozHCvrT2H-qPacU0-5uSCJW_HxVnpQyLsA88kqM/edit?usp=sharing"

# Fetch the contact data from Google Sheets
contacts = fetch_contact_data(sheet_url)

# Streamlit layout for displaying contacts
st.title("ทำเนียบนายทหาร จปร. ค่ายสุรสีห์")

# Search inputs with categories (ตำแหน่ง field removed)
name_search = st.text_input("ค้นหาด้วยชื่อ")
unit_search = st.text_input("ค้นหาด้วยหน่วย")
rank_search = st.text_input("ค้นหาด้วยยศ")

# Add a search button
search_clicked = st.button("ค้นหา")

# Perform search and display results only if the search button is clicked
if search_clicked:
    # Perform search based on input
    search_results = []
    for contact in contacts:
        # Convert phone number to string with leading zeros
        phone_number = format_phone_number(contact['โทรศัพท์'])

        # Check if search criteria match (name, unit, rank)
        if (name_search.lower() in (contact['ยศ ชื่อ สกุล'].lower() + contact['ชื่อเล่น'].lower())) and \
           (unit_search.lower() in contact['ตำแหน่ง'].lower()) and \
           (rank_search.lower() in contact['ยศ ชื่อ สกุล'].lower()):
            search_results.append(contact)

    # Display contacts in a frame
    if search_results:
        for contact in search_results:
            st.markdown(f"""
            <div style="border: 2px solid #d4d4d4; padding: 15px; margin-bottom: 15px;">
                <div style="text-align: center;">
                    <img src="{contact['ภาพ']}" alt="Contact Image" width="150" style="margin-bottom: 15px;">
                </div>
                <div style="text-align: center; padding-bottom: 15px;">
                    <div style='font-size:20px; line-height:2'>
                        <strong>รุ่น:</strong> {contact['รุ่น']}<br>
                        <strong>ยศ-ชื่อ:</strong> {contact['ยศ ชื่อ สกุล']}<br>
                        <strong>ชื่อเล่น:</strong> {contact['ชื่อเล่น']}<br>
                        <strong>ตำแหน่ง:</strong> {contact['ตำแหน่ง']}<br>
                        <strong>โทรศัพท์:</strong> {phone_number}<br>
                        <strong>วัน เดือน ปี เกิด:</strong> {contact['วัน เดือน ปี เกิด']}<br>
                    </div>
                </div>
                <div style="text-align: center;">
                    <a href="tel:{phone_number}" style="text-decoration: none;">
                        <button style="background-color: #4CAF50; color: white; padding: 10px 24px; border: none; cursor: pointer;">
                            Call
                        </button>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("ไม่พบข้อมูลที่ต้องการค้นหา")
