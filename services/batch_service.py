import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import re
import requests

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


# ----------------------------------------------------------
# Extract REAL hyperlinks using Google Sheets API
# ----------------------------------------------------------
def get_hyperlinks_from_sheet():
    service = build("sheets", "v4", credentials=creds)

    spreadsheet = service.spreadsheets().get(
        spreadsheetId=sheet.spreadsheet.id,
        includeGridData=True
    ).execute()

    grid = spreadsheet["sheets"][0]["data"][0]["rowData"]

    links_map = []

    for row in grid:
        row_links = []
        for cell in row.get("values", []):
            url = None

            # Case 1: direct cell-wide hyperlink
            if "hyperlink" in cell:
                url = cell["hyperlink"]

            # Case 2: rich text links inside the cell
            if "textFormatRuns" in cell:
                for run in cell["textFormatRuns"]:
                    if "format" in run and "link" in run["format"]:
                        url = run["format"]["link"].get("uri")

            row_links.append(url)
        links_map.append(row_links)

    return links_map


# ----------------------------------------------------------
# Extract URL from =HYPERLINK() formulas
# ----------------------------------------------------------
def extract_url(cell_value: str):
    match = re.search(r'HYPERLINK\("([^"]+)"', cell_value)
    if match:
        return match.group(1)
    return cell_value  # fallback (maybe plain URL)


# ----------------------------------------------------------
# Check reachable links
# ----------------------------------------------------------
def check_link(input_text: str):
    url_regex = re.compile(
        r'^(https?://)'         # MUST start with http/https for safety
        r'([\w.-]+)'            # domain
        r'(\.[a-zA-Z]{2,})'     # .com .in etc.
        r'(/.*)?$'              # path
    )

    if not url_regex.match(input_text):
        return False

    try:
        r = requests.head(input_text, allow_redirects=True, timeout=5)
        return r.status_code == 200
    except:
        return False


# ----------------------------------------------------------
# Main function
# ----------------------------------------------------------
def get_row_by_lot_number(lot_number: str):

    if not lot_number:
        return {"error": "Missing lot number"}

    # Get displayed/formula values
    values_list = sheet.get_values(value_render_option="FORMULA")

    # Get actual hyperlinks from metadata
    hyperlink_map = get_hyperlinks_from_sheet()

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
    row_index = values_list.index(row)

    response_arr = []

    for col_index, cell in enumerate(row):
        # Prefer hyperlink metadata → fallback to formula → fallback to plain text
        real_value = hyperlink_map[row_index][col_index] or extract_url(cell)

        if check_link(real_value):
            response_arr.append(real_value)

    if len(response_arr) == 0:
        print("Row without links:", row)
        return {"error": "No valid links found"}

    return {
        "links": response_arr
    }