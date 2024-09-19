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

# Step 4: Centered content layout
st.markdown("""
    <style>
    .centered-content {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Step 5: Filter and display search results in custom layout
if search_term:
    # Search for the term across all columns
    search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    
    # Display the results
    if not search_results.empty:
        st.write(f"พบผลลัพธ์ที่ค้นหา (Search Results) for '{search_term}':")
        
        # Loop through each row in search results and display in custom layout
        for _, contact in search_results.iterrows():
            phone_number = format_phone_number(contact['โทรศัพท์'])  # Ensure phone number has 10 digits
            
            # Create columns for centered layout
            col1, col2, col3 = st.columns([1, 2, 1])  # The second column will hold the content in the center
            
            with col2:  # Center content in the middle column
                with st.container():
                    st.markdown('<div class="centered-content">', unsafe_allow_html=True)
                    st.image(contact['ภาพ'], width=150)  # Display image
                    st.write(f"**ยศ ชื่อ สกุล**: {contact['ยศ ชื่อ สกุล']}")
                    st.write(f"**ชื่อเล่น**: {contact['ชื่อเล่น']}")
                    st.write(f"**รุ่น**: {contact['รุ่น']}")
                    st.write(f"**ตำแหน่ง**: {contact['ตำแหน่ง']}")
                    st.write(f"**วัน เดือน ปี เกิด**: {contact['วัน เดือน ปี เกิด']}")
                    st.write(f"**หมายเลขโทรศัพท์**: {phone_number}")
                    st.markdown('</div>', unsafe_allow_html=True)
                st.write("---")  # Separator between entries
    else:
        st.write("ไม่พบข้อมูลที่ต้องการ (No matching data found)")
