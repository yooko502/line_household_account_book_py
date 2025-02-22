from flask import Flask
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, MessageAction, RichMenuSize
import os
from linebot import LineBotApi, WebhookHandler

configuration = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
line_handler = WebhookHandler(os.environ['CHNNEL_SECRET_TOKEN'])

def create_rich_menu():
    rich_menu_to_create = RichMenu(
        size = RichMenuSize(height=1686,width=2500),
        selected=False,
        name="Rich menu",
        chat_bar_text="Tap here",
        areas=[
                    RichMenuArea(
                        bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
                        action=MessageAction(label='Person Form', text='個人登録')
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=1251, y=0, width=1250, height=843),
                        action=MessageAction(label='Group Form', text='グループ登録')
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=0, y=843, width=844, height=843),
                        action=MessageAction(label='Total', text='合計')
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=1251, y=843, width=832, height=843),
                        action=MessageAction(label='Financial', text='消費分析')
                    )
                ]
    )
    try:
        rich_menu_id = configuration.create_rich_menu(rich_menu=rich_menu_to_create)
        print(f"Rich Menu created with ID: {rich_menu_id}")
    except Exception as e:
        print(f"Error creating rich menu: {e}")
        return

    try:
        with open("static/richmessage.png", 'rb') as f:
            configuration.set_rich_menu_image(rich_menu_id, 'image/png', f)
        print("Rich Menu image uploaded")
    except Exception as e:
        print(f"Error uploading image: {e}")
        return

    try:
        configuration.set_default_rich_menu(rich_menu_id)
        print("Rich Menu set as default")
    except Exception as e:
        print(f"Error setting default rich menu: {e}")