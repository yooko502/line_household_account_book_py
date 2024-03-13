import gspread
from oauth2client.service_account import ServiceAccountCredentials


SHEET_CELL = {
    "DATA": 1,
    "MEMO": 2,
    "AMOUNT": 3
}
def connect_gspread(jsonf, key, json_message):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    ws = gc.open_by_key(SPREADSHEET_KEY).sheet1
    # ws = connect_gspread(jsonf, spread_sheet_key)
    data = ws.get_all_values()
    row_number = len(data)
    ws.update_cell(row_number + 1, SHEET_CELL['DATA'] , json_message['date'])
    ws.update_cell(row_number + 1, SHEET_CELL['MEMO'], json_message['memo'])
    ws.update_cell(row_number + 1, SHEET_CELL['AMOUNT'], json_message['amount'])