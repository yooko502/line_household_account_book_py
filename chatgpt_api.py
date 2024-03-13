from openai import OpenAI
import os
import json

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI()
client.api_key = OPENAI_API_KEY

def get_chatgpt_message(user_message):
    schema = {
    "date": "YYYY-MM-DD",
    "amount": "number",
    "memo": "string"
    }
    response = client.chat.completions.create(
            model = 'gpt-3.5-turbo',
            response_format={"type": "json_object"},
            messages = [
                {
                    'role': 'system',
                    'content': f"从以下字符串中提取date,amount,memo相关信息,date的格式为'YYYY-MM-DD',如果信息中不包含年份,补全为2024,并以json格式输出。JSON SCHEMA如下:{schema}"
                }
                , {
                    'role': 'user'
                    , 'content': user_message
                }
            ]
        )

    json_message = json.loads(response.choices[0].message.content)
    return json_message