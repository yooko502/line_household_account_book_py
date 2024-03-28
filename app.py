from flask import Flask, render_template, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
from chatgpt_api import get_chatgpt_message
from google_sheet_api import get_total, update_google_sheet_content, get_users_sheet_key, update_users_sheet_key
import re

from line_rich_menu_api import create_rich_menu

app = Flask(__name__, template_folder='templates')

configuration = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
line_handler = WebhookHandler(os.environ['CHNNEL_SECRET_TOKEN'])

# spread_sheet_key = os.environ['SPREAD_SHEET_KEY']

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
        user_id = None
        if event.source.type == 'user':
            user_id = event.source.user_id
        user_message = event.message.text
        if user_id is None:
            configuration.reply_message(event.reply_token, TextSendMessage(text="请登录"))
            return
        # rich menu event for person
        if user_message == '個人登録':
            message = TemplateSendMessage(
                alt_text='Please input your google sheet key',
                template=ButtonsTemplate(
                    text='あなたのGoogle sheet key登録してください',
                    actions=[
                        URIAction(label='個人Google Sheet登録', uri=f'https://line-household-account-book-py.onrender.com/person_form?line_user_id={user_id}')
                    ]
                )
            )
            # 发送消息给用户
            configuration.reply_message(event.reply_token, message)
            return
        
        if user_message == 'グループ登録':
            message = TemplateSendMessage(
                alt_text='Please input your google sheet key',
                template=ButtonsTemplate(
                    text='グループのGoogle sheet key登録してください',
                    actions=[
                        URIAction(label='グループGoogle Sheet登録', uri=f'https://line-household-account-book-py.onrender.com/group_form?line_user_id={user_id}')
                    ]
                )
            )
            # 发送消息给用户
            configuration.reply_message(event.reply_token, message)
            return

        user_google_sheet_key, username = get_users_sheet_key(user_id)

        if user_message == '合計':
            total = get_total(user_google_sheet_key)
            return_message = \
            f"""=== 已消费 ===\n{str(total)}"""
            configuration.reply_message(event.reply_token, TextSendMessage(text=return_message))
            return

        # 调用chat gpt 进行分类
        json_message = get_chatgpt_message(user_message)

        # 把信息登录到google sheet
        update_google_sheet_content(user_google_sheet_key, json_message, username)
        return_message = \
        f"""=== 账单已登录 ===\n日期: {json_message['date']}\n消费内容: {json_message['memo']}\n金额: {json_message['amount']}"""
        configuration.reply_message(event.reply_token, TextSendMessage(text=return_message))

@app.route("/person_form", methods=["GET"])
def person_form():
     line_user_id = request.args.get('line_user_id')
     return render_template("person_form.html", line_user_id=line_user_id)

@app.route('/person_submit', methods=['POST'])
def submit():
    person_key = request.form.get('person_key')
    user_id = request.form.get('line_user_id')
    update_users_sheet_key(user_id, person_key)
    return "あなたのGoogle sheet登録しました。"

@app.route("/group_form", methods=["GET"])
def group_form():
     line_user_id = request.args.get('line_user_id')
     return render_template("group_form.html", line_user_id=line_user_id)

@app.route('/group_submit', methods=['POST'])
def group_submit():
    group_key = request.form.get('group_key')
    user_id = request.form.get('line_user_id')
    username = request.form.get('username')
    update_users_sheet_key(user_id, group_key, username)
    return "グループのGoogle sheet登録しました。"

create_rich_menu()
if __name__ == "__main__":
      app.run(host="0.0.0.0", port=10000, debug=True)