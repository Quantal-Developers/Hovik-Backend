import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

# Google API Scopes
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly"
]

# Auth
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Load sheet
SHEET_NAME = os.getenv("SHEET_NAME", "BATCH_details")
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME", "Sheet1")

sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)


def get_row_by_lot_number(lot_number: str):

    values_list = sheet.get_all_values()
    
    if not lot_number:
        return {"error": "Missing lot number"}
    
    lot_number = lot_number.strip()
    matches = []

    for row in values_list:
        if row[0].strip().upper() == lot_number.upper():
            matches.append(row)

    if not matches:
        return {"error": "Lot number not found"}

    if len(matches) > 1:
        return {
            "error": "Multiple rows found for this lot number",
            "count": len(matches)
        }
    
    row = matches[0]
    
    return {
        "BATCH": row[0],
        "LINK1": row[1],
        "LINK2": row[2]
    }
