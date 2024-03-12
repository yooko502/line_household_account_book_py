from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from openai import OpenAI
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

configuration = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
line_handler = WebhookHandler(os.environ['CHNNEL_SECRET_TOKEN'])
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
spread_sheet_key = os.environ['SPREAD_SHEET_KEY']
client = OpenAI()
client.api_key = OPENAI_API_KEY

schema = {
    "date": "YYYY-MM-DD",
    "amount": "number",
    "memo": "string"
}

SHEET_CELL = {
    "DATA": 1,
    "MEMO": 2,
    "AMOUNT": 3
}

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
        response = client.chat.completions.create(
            model = 'gpt-3.5-turbo',
            response_format={"type": "json_object"},
            messages = [
                {
                    'role': 'system'
                    , 'content': f"从以下字符串中提取date,amount,memo相关信息，并以json格式输出。JSON SCHEMA如下：{schema}"
                }
                , {
                    'role': 'user'
                    , 'content': user_message
                }
            ]
        )

        json_message = json.loads(response.choices[0].message.content)
        jsonf = "/etc/secrets/GOOGLE_SECRETS_JSON"
        ws = connect_gspread(jsonf, spread_sheet_key)
        data = ws.get_all_values()
        row_number = len(data)
        ws.update_cell(row_number + 1, SHEET_CELL['DATA'] , json_message['date'])
        ws.update_cell(row_number + 1, SHEET_CELL['MEMO'], json_message['memo'])
        ws.update_cell(row_number + 1, SHEET_CELL['AMOUNT'], json_message['amount'])

        configuration.reply_message(event.reply_token, TextSendMessage(text=response.choices[0].message.content))

def connect_gspread(jsonf,key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = key
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

    return worksheet

if __name__ == "__main__":
      app.run(host="0.0.0.0", port=10000, debug=True)