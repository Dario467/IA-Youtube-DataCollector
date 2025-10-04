import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# the credential is like the api key, but we call the json and the scope
creds = Credentials.from_service_account_info(st.secrets["google_credentials"],
                                              scopes=["https://www.googleapis.com/auth/spreadsheets"])
# Access authorization, Authorize the credential
client = gspread.authorize(creds)
# Access a specific sheet
sheet_id = st.secrets["SHEET_ID"]
# Open de sheet
sheet = client.open_by_key(sheet_id)
# Open sheet 1
sheet1 = sheet.sheet1
# Open sheet 2
sheet2 = sheet.get_worksheet(1)
