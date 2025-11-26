import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
load_dotenv()
sheet_id = os.environ['sheet_id'] 
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet = client.open_by_key(sheet_id)
values_list = sheet.sheet1.row_values(1)

print(values_list)