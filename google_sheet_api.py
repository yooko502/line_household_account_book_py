import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_CELL = {
    "DATA": 1,
    "MEMO": 2,
    "AMOUNT": 3
}
jsonf = "/etc/secrets/GOOGLE_SECRETS_JSON"

# 更新每个人的表单
def connect_gspread(key, json_message):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    ws = gc.open_by_key(SPREADSHEET_KEY).sheet1
    # ws = connect_gspread(jsonf, spread_sheet_key)
    data = ws.get_all_values()
    row_number = len(data)
    if ws.is_empty():
        ws.update_cell(1, 1 , '日期')
        ws.update_cell(1, 2 , '花销内容')
        ws.update_cell(1, 3 , '金额')
        ws.format(row=1, col=1, backgroundColor="#3CB371")
        ws.format(row=1, col=2, backgroundColor="#3CB371")
        ws.format(row=1, col=3, backgroundColor="#3CB371")
        ws.update_cell(row_number + 1, SHEET_CELL['DATA'] , json_message['date'])
        ws.update_cell(row_number + 1, SHEET_CELL['MEMO'], json_message['memo'])
        ws.update_cell(row_number + 1, SHEET_CELL['AMOUNT'], json_message['amount'])
    else:
        ws.update_cell(row_number + 1, SHEET_CELL['DATA'] , json_message['date'])
        ws.update_cell(row_number + 1, SHEET_CELL['MEMO'], json_message['memo'])
        ws.update_cell(row_number + 1, SHEET_CELL['AMOUNT'], json_message['amount'])

# 将用户的key登录
def update_users_sheet_key(user_id, google_sheet_key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    # 记录数据用的表单key
    SPREADSHEET_KEY = os.environ['SPREAD_SHEET_KEY']
    ws = gc.open_by_key(SPREADSHEET_KEY).sheet1
    # ws = connect_gspread(jsonf, spread_sheet_key)
    data = ws.get_all_values()
    row_number = len(data)
    user_cell = ws.find(user_id)
    if ws.is_empty():
        ws.update_cell(1, 1 , 'user_id')
        ws.update_cell(1, 2 , 'user_key')
        ws.update_cell(row_number + 1, 1 , user_id)
        ws.update_cell(row_number + 1, 2 , google_sheet_key)
    elif user_cell is not None:
        # 同一个用户更新为新的表单
        ws.update_cell(user_cell.row, user_cell.col + 1, google_sheet_key)
    else:
        ws.update_cell(row_number + 1, 1 , user_id)
        ws.update_cell(row_number + 1, 2 , google_sheet_key)

# 获取用户key
def get_users_sheet_key(user_id):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = os.environ['SPREAD_SHEET_KEY']
    ws = gc.open_by_key(SPREADSHEET_KEY).sheet1
    # ws = connect_gspread(jsonf, spread_sheet_key)
    user_cell = ws.find(user_id)
    google_sheet_key_cell = ws.cell(user_cell.row, user_cell.col + 1).value

    return google_sheet_key_cell