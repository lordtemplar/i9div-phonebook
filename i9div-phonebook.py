import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Set page title
st.set_page_config(page_title="Google Sheets Data Fetch")

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

# Step 3: Display data in Streamlit
try:
    df = fetch_data_from_google_sheets(sheet_url)
    st.write("Data fetched from Google Sheets:")
    st.dataframe(df)  # Display the data as a Streamlit DataFrame
except Exception as e:
    st.error(f"Error fetching data: {e}")

