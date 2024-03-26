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
    prompt = f"""
        Your task is to perform the following actions: \
        1 - Analyze the information in the text and extract the date, amount, and consumption content \
        2 - If the date provided by the text does not contain year information, use YYYY instead of the year. \
        3 - The date format is generated in YYYY/MM/DD \
        Use the following json_object format:\
        {schema}
        Text: <{user_message}>
    """
    response = client.chat.completions.create(
            model = 'gpt-4-turbo-preview',
            response_format={"type": "json_object"},
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages = [
                {
                    'role': 'system',
                    'content': prompt
                }
                , {
                    'role': 'user'
                    , 'content': user_message
                }
            ]
        )
    json_message = json.loads(response.choices[0].message.content)
    if json_message['date'] == "YYYY-MM-DD":
        json_message['date'] = datetime.date.today().strftime("%Y/%m/%d")
    if json_message['date'].startswith("YYYY"):
        current_year = datetime.datetime.now().year
        json_message['date'] = json_message['date'].replace("YYYY", str(current_year))

    return json_message