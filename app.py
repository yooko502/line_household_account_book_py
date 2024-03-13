from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
from chatgpt_api import get_chatgpt_message
from google_sheet_api import connect_gspread

app = Flask(__name__)

configuration = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
line_handler = WebhookHandler(os.environ['CHNNEL_SECRET_TOKEN'])

spread_sheet_key = os.environ['SPREAD_SHEET_KEY']

@app.route('/', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    try:
        line_handler.handle(body, signature)
        app.logger.debug("Request body: " + body)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        user_message = event.message.text
        json_message = get_chatgpt_message(user_message)
        jsonf = "/etc/secrets/GOOGLE_SECRETS_JSON"
        connect_gspread(jsonf, spread_sheet_key, json_message)
        return_message = f"""
            === 账单已登录 ===
            日期: {json_message['date']}
            消费内容: {json_message['memo']}
            金额: {json_message['amount']}
        """
        configuration.reply_message(event.reply_token, TextSendMessage(text=return_message))

# def connect_gspread(jsonf, key, json_message):
#     scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#     credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
#     gc = gspread.authorize(credentials)
#     SPREADSHEET_KEY = key
#     ws = gc.open_by_key(SPREADSHEET_KEY).sheet1
#     # ws = connect_gspread(jsonf, spread_sheet_key)
#     data = ws.get_all_values()
#     row_number = len(data)
#     ws.update_cell(row_number + 1, SHEET_CELL['DATA'] , json_message['date'])
#     ws.update_cell(row_number + 1, SHEET_CELL['MEMO'], json_message['memo'])
#     ws.update_cell(row_number + 1, SHEET_CELL['AMOUNT'], json_message['amount'])

if __name__ == "__main__":
      app.run(host="0.0.0.0", port=10000, debug=True)