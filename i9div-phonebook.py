import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

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

# Fetch contact data from Google Sheets and store in a DataFrame
def fetch_contact_data(sheet_url):
    client = authenticate_google_sheets()
    sheet = client.open_by_url(sheet_url).sheet1  # Access the first sheet
    data = sheet.get_all_records()  # Fetch all records
    df = pd.DataFrame(data)  # Convert data to DataFrame
    return df

# Function to ensure the phone number has a leading zero
def format_phone_number(phone_number):
    phone_number_str = str(phone_number)
    if len(phone_number_str) == 9:
        return '0' + phone_number_str
    return phone_number_str

# URL for the Google Sheets containing contact data
sheet_url = "https://docs.google.com/spreadsheets/d/1bN11ozHCvrT2H-qPacU0-5uSCJW_HxVnpQyLsA88kqM/edit?usp=sharing"

# Fetch the contact data from Google Sheets and store in a DataFrame
contacts_df = fetch_contact_data(sheet_url)

# Streamlit layout for displaying contacts
st.title("ทำเนียบนายทหาร จปร. ค่ายสุรสีห์")

# Search inputs with categories
name_search = st.text_input("ค้นหาด้วยชื่อ")
unit_search = st.text_input("ค้นหาด้วยหน่วย")
rank_search = st.text_input("ค้นหาด้วยยศ")

# Add a search button
search_clicked = st.button("ค้นหา")

# Perform search and display results only if the search button is clicked
if search_clicked:
    # Perform search based on input
    search_results = contacts_df[
        (contacts_df['ยศ ชื่อ สกุล'].str.contains(name_search, case=False, na=False)) |
        (contacts_df['ชื่อเล่น'].str.contains(name_search, case=False, na=False))
    ]
    
    # Filter by unit and rank if provided
    if unit_search:
        search_results = search_results[search_results['ตำแหน่ง'].str.contains(unit_search, case=False, na=False)]
    if rank_search:
        search_results = search_results[search_results['ยศ ชื่อ สกุล'].str.contains(rank_search, case=False, na=False)]

    # Display contacts in a frame
    if not search_results.empty:
        for _, contact in search_results.iterrows():
            phone_number = format_phone_number(contact['โทรศัพท์'])
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
                    <button id="copy-button-{contact.name}" onclick="copyToClipboard('{phone_number}')"
                    style="background-color: #4CAF50; color: white; padding: 10px 24px; border: none; cursor: pointer;">
                        คัดลอกเบอร์โทรศัพท์
                    </button>
                </div>
            </div>

            <script>
            function copyToClipboard(text) {{
                navigator.clipboard.writeText(text).then(function() {{
                    alert('คัดลอกเบอร์โทรศัพท์แล้ว: ' + text);
                }}, function(err) {{
                    console.error('ไม่สามารถคัดลอกเบอร์ได้', err);
                }});
            }}
            </script>
            """, unsafe_allow_html=True)
    else:
        st.warning("ไม่พบข้อมูลที่ต้องการค้นหา")
