import gspread
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SHEET_URL = "https://docs.google.com/spreadsheets/d/1o0lFaYlVnSvIuXfe7jdI1_LQSCVwBUosto_mhjz_d5U/edit?gid=0#gid=0"

def get_sheet():
    creds = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )

    client = gspread.authorize(creds)

    return client.open_by_url(SHEET_URL).sheet1