from flask import Flask
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, MessageAction, RichMenuSize
import os
from linebot import LineBotApi, WebhookHandler

configuration = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
line_handler = WebhookHandler(os.environ['CHNNEL_SECRET_TOKEN'])

def create_rich_menu():
    rich_menu_to_create = RichMenu(
        size = RichMenuSize(height=843,width=2500),
        selected=False,
        name="Rich menu",
        chat_bar_text="Tap here",
        areas=[
                    RichMenuArea(
                        bounds=RichMenuBounds(x=0, y=0, width=834, height=843),
                        action=MessageAction(label='Person Form', text='個人登録')
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=835, y=0, width=834, height=843),
                        action=MessageAction(label='Group Form', text='グループ登録')
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=1669, y=0, width=832, height=843),
                        action=MessageAction(label='Total', text='合計')
                    )
                ]
    )

    rich_menu_id = configuration.create_rich_menu(rich_menu=rich_menu_to_create)

    with open("static/richmessage.png", 'rb') as f:
        configuration.set_rich_menu_image(rich_menu_id, 'image/png', f)

    configuration.set_default_rich_menu(rich_menu_id)