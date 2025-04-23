import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SHEET_NAME = "Sorted Leads"
TAB_NAME = "FilteredLeads"

def get_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/creds.json", SCOPE)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).worksheet(TAB_NAME)

def get_unsent_leads():
    sheet = get_sheet()
    data = sheet.get_all_records()
    return [(i + 2, row) for i, row in enumerate(data) if str(row.get("Status", "")).strip().lower() in ["", "no"]]


def update_status(row_number, status):
    sheet = get_sheet()
    sheet.update_cell(row_number, 5, status)  # Status is column 5 (E)
