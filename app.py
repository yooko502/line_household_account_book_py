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
        # 调用chat gpt 进行分类
        json_message = get_chatgpt_message(user_message)
        jsonf = "/etc/secrets/GOOGLE_SECRETS_JSON"
        # 把信息登录到google sheet
        # TODO: 1. line menu 接受用户的表格id，根据用户来更新用户的表格（spread_sheet_key 需要替换为用户的）
        connect_gspread(jsonf, spread_sheet_key, json_message)
        # line bot 返回信息
        return_message = \
        f"""=== 账单已登录 ===\n日期: {json_message['date']}\n消费内容: {json_message['memo']}\n金额: {json_message['amount']}"""
        configuration.reply_message(event.reply_token, TextSendMessage(text=return_message))

if __name__ == "__main__":
      app.run(host="0.0.0.0", port=10000, debug=True)