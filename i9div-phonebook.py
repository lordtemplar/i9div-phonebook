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

# Google Sheet URL
sheet_url = "https://docs.google.com/spreadsheets/d/1bN11ozHCvrT2H-qPacU0-5uSCJW_HxVnpQyLsA88kqM/edit?usp=sharing"

# Step 3: Fetch the data
df = fetch_data_from_google_sheets(sheet_url)

# Search box to search across the entire DataFrame
search_term = st.text_input("ค้นหา (Search)")

# Step 4: Filter and display search results
if search_term:
    # Search for the term across all columns
    search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    
    # Display the results
    if not search_results.empty:
        st.write(f"พบผลลัพธ์ที่ค้นหา (Search Results) for '{search_term}':")
        st.dataframe(search_results)  # Display matching rows
    else:
        st.write("ไม่พบข้อมูลที่ต้องการ (No matching data found)")
