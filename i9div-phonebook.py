import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Set page title
st.set_page_config(page_title="Google Sheets Search")

# Step 1: Connect to Google Sheets using credentials
def authenticate_google_sheets():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],  # Add your credentials to Streamlit secrets
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    client = gspread.authorize(credentials)
    return client

# Step 2: Fetch data from a Google Sheet and load into a pandas DataFrame
def fetch_data_from_google_sheets(sheet_url):
    client = authenticate_google_sheets()
    sheet = client.open_by_url(sheet_url).sheet1  # Open the first sheet
    data = sheet.get_all_records()  # Fetch all records as a list of dictionaries
    df = pd.DataFrame(data)  # Convert to a pandas DataFrame
    return df

# Ensure phone number has a leading zero if required
def format_phone_number(phone_number):
    phone_number_str = str(phone_number)
    return '0' + phone_number_str if len(phone_number_str) == 9 else phone_number_str

# Google Sheet URL
sheet_url = "https://docs.google.com/spreadsheets/d/1bN11ozHCvrT2H-qPacU0-5uSCJW_HxVnpQyLsA88kqM/edit?usp=sharing"

# Step 3: Fetch the data
df = fetch_data_from_google_sheets(sheet_url)

# Search box to search across the entire DataFrame
search_term = st.text_input("ค้นหา (Search)")

# Apply custom CSS to center content within each column and ensure visibility in dark themes
st.markdown("""
    <style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
    }
    .center-content {
        width: 100%;
        max-width: 600px;
        margin: auto;
        background-color: #2d2d2d;  /* Dark background for dark theme */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        color: #f1f1f1;  /* Light text color for dark theme */
    }
    h3, p {
        color: #f1f1f1;  /* Ensure all text is light-colored */
    }
    </style>
""", unsafe_allow_html=True)

# Step 4: Filter and display search results in custom layout
if search_term:
    # Search for the term across all columns
    search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    
    # Display the results
    if not search_results.empty:
        st.write(f"พบผลลัพธ์ที่ค้นหา (Search Results) for '{search_term}':")
        
        # Loop through each row in search results and display in custom layout
        for _, contact in search_results.iterrows():
            phone_number = format_phone_number(contact['โทรศัพท์'])  # Ensure phone number has 10 digits
            
            # Create container div to center content both horizontally and vertically
            st.markdown('<div class="container">', unsafe_allow_html=True)
            
            # Each contact info block
            st.markdown(f"""
                <div class="center-content">
                    <img src="{contact['ภาพ']}" width="150" style="border-radius: 50%; margin-bottom: 20px;">
                    <h3>{contact['ยศ ชื่อ สกุล']}</h3>
                    <p><strong>ชื่อเล่น:</strong> {contact['ชื่อเล่น']}</p>
                    <p><strong>รุ่น:</strong> {contact['รุ่น']}</p>
                    <p><strong>ตำแหน่ง:</strong> {contact['ตำแหน่ง']}</p>
                    <p><strong>วัน เดือน ปี เกิด:</strong> {contact['วัน เดือน ปี เกิด']}</p>
                    <p><strong>หมายเลขโทรศัพท์:</strong> {phone_number}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)  # Close container div

    else:
        st.write("ไม่พบข้อมูลที่ต้องการ (No matching data found)")
