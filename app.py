from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from openai import OpenAI
import os

app = Flask(__name__)

configuration = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
line_handler = WebhookHandler(os.environ['CHNNEL_SECRET_TOKEN'])
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI()
client.api_key = OPENAI_API_KEY

schema = {
    "date": "YYYY-MM-DD",
    "amount": "number",
    "memo": "string"
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
        user_message = TextSendMessage(text=event.message.text)
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

        configuration.reply_message(event.reply_token, TextSendMessage(text=response.choices[0].message.content))

if __name__ == "__main__":
      app.run(host="0.0.0.0", port=10000, debug=True)