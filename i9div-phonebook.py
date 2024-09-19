import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from st_copy_to_clipboard import st_copy_to_clipboard  # Import the copy-to-clipboard component

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

    # Display contacts using Streamlit's native components
    if not search_results.empty:
        for _, contact in search_results.iterrows():
            phone_number = format_phone_number(contact['โทรศัพท์'])
            
            # Display the photo
            st.image(contact['ภาพ'], width=150)

            # Display details in the specified order
            st.write(f"**ยศ-ชื่อ**: {contact['ยศ ชื่อ สกุล']}")
            st.write(f"**ชื่อเล่น**: {contact['ชื่อเล่น']}")
            st.write(f"**รุ่น**: {contact['รุ่น']}")
            st.write(f"**ตำแหน่ง**: {contact['ตำแหน่ง']}")
            st.write(f"**วัน เดือน ปี เกิด**: {contact['วัน เดือน ปี เกิด']}")
            st.write(f"**โทรศัพท์**: {phone_number}")
            
            # Add the Copy to Clipboard button with a label
            st_copy_to_clipboard(phone_number, label="คัดลอกหมายเลขโทรศัพท์")

            if st.button("คัดลอกหมายเลขโทรศัพท์"):
                js = f"""
                <script>
                    navigator.clipboard.writeText('{phone_number}').then(function() {{
                        alert('คัดลอกหมายเลขโทรศัพท์: {phone_number}');
                    }}, function(err) {{
                        console.error('ไม่สามารถคัดลอกได้:', err);
                    }});
                </script>
                """
                st.components.v1.html(js)

            st.write("---")  # Separator line for each contact
    else:
        st.warning("ไม่พบข้อมูลที่ต้องการค้นหา")
