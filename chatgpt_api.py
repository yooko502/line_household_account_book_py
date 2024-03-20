import datetime
from openai import OpenAI
import os
import json

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI()
client.api_key = OPENAI_API_KEY

def get_chatgpt_message(user_message):
    schema = {
    "date": "YYYY/MM/DD",
    "amount": "number",
    "memo": "string"
    }
    response = client.chat.completions.create(
            model = 'gpt-3.5-turbo',
            response_format={"type": "json_object"},
            messages = [
                {
                    'role': 'system',
                    'content': f"从以下字符串中提取date,amount,memo相关信息,如果不含date信息,则date补充为空值,JSON SCHEMA如下:{schema}"
                }
                , {
                    'role': 'user'
                    , 'content': user_message
                }
            ]
        )
    json_message = json.loads(response.choices[0].message.content)
    if not json_message.get('date'):
        json_message['date'] = datetime.date.today().strftime("%Y/%m/%d")
    if json_message['date'].startswith("YYYY"):
        current_year = datetime.datetime.now().year
        json_message['date'] = json_message['date'].replace("YYYY", str(current_year))

    return json_message