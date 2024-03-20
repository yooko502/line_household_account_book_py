from flask import Flask
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, URIAction, MessageAction, RichMenuSize
import os
from linebot import LineBotApi, WebhookHandler

configuration = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
line_handler = WebhookHandler(os.environ['CHNNEL_SECRET_TOKEN'])

def create_rich_menu():
    rich_menu_to_create = RichMenu(
        size = RichMenuSize(height=585,width=1040),
        selected=True,
        name="Rich menu",
        chat_bar_text="Tap here",
        areas=[
                    RichMenuArea(
                        bounds=RichMenuBounds(x=0, y=0, width=520, height=585),
                        action=MessageAction(label='person', text='Hello, World!')
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=520, y=0, width=520, height=585),
                        action=MessageAction(label='group', text='Hello, World!2')
                    )
                ]
    )

    rich_menu_id = configuration.create_rich_menu(rich_menu=rich_menu_to_create)

    with open("static/richmessage.png", 'rb') as f:
        configuration.set_rich_menu_image(rich_menu_id, 'image/png', f)

    configuration.set_default_rich_menu(rich_menu_id)