from flask import Flask
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, MessageAction, RichMenuSize
import os
from linebot import LineBotApi, WebhookHandler
from linebot.v3.messaging import (
    CreateRichMenuAliasRequest
)

configuration = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
line_handler = WebhookHandler(os.environ['CHNNEL_SECRET_TOKEN'])

def create_rich_menu():
    rich_menu_to_create = RichMenu(
        size = RichMenuSize(height=585,width=1040),
        selected=False,
        name="Rich menu",
        chat_bar_text="Tap here",
        areas=[
                    RichMenuArea(
                        bounds=RichMenuBounds(x=0, y=0, width=520, height=585),
                        action=MessageAction(label='Person Form', text='個人登録')
                    ),
                    RichMenuArea(
                        bounds=RichMenuBounds(x=521, y=0, width=520, height=585),
                        action=MessageAction(label='Group Form', text='グループ登録')
                    )
                ]
    )

    total_rich_menu_to_create = RichMenu(
        size = RichMenuSize(height=585,width=1040),
        selected=False,
        name="Total Rich menu",
        chat_bar_text="合計",
        areas=[
                    RichMenuArea(
                        bounds=RichMenuBounds(x=0, y=0, width=1040, height=585),
                        action=MessageAction(label='Person Form', text='合計')
                    ),
                ]
    )

    rich_menu_id = configuration.create_rich_menu(rich_menu=rich_menu_to_create)
    total_rich_menu_id = configuration.create_rich_menu(rich_menu=total_rich_menu_to_create)

    with open("static/richmessage.png", 'rb') as f:
        configuration.set_rich_menu_image(rich_menu_id, 'image/png', f)
    
    with open("static/richmenu_total.png", 'rb') as f:
        configuration.set_rich_menu_image(total_rich_menu_id, 'image/png', f)

    configuration.set_default_rich_menu(rich_menu_id)
    configuration.set_default_rich_menu(total_rich_menu_id)

    alias_a = CreateRichMenuAliasRequest(
            rich_menu_alias_id='richmenu-alias-a',
            rich_menu_id=rich_menu_id
        )
    configuration.create_rich_menu_alias(alias_a)

    alias_b = CreateRichMenuAliasRequest(
            rich_menu_alias_id='richmenu-alias-b',
            rich_menu_id=total_rich_menu_id
        )
    configuration.create_rich_menu_alias(alias_b)