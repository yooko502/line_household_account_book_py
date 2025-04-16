import datetime
from openai import OpenAI
import os
import json

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI()
client.api_key = OPENAI_API_KEY
client.base_url = "https://api.deepseek.com/v1"

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
            model = 'deepseek-chat',
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
    if json_message['date'] == "YYYY/MM/DD":
        json_message['date'] = datetime.date.today().strftime("%Y/%m/%d")
    if json_message['date'].startswith("YYYY"):
        current_year = datetime.datetime.now().year
        json_message['date'] = json_message['date'].replace("YYYY", str(current_year))

    return json_message

def financial_analysis_gpt_message(user_message):
        prompt = f"""
                    你是一个专业的财务分析师，根据提供的数据，从衣，食，住，行，玩五个方面，总结出消费习惯，总结内容遵循以下模板。
                    ### 食
                    - **主要消费内容**：吃饭和买菜是最主要的消费内容，便利店购买午饭也有记录。
                    - **主要消费场所**：主要是餐厅和便利店。
                    - **最高消费价格**：800元（在2024-03-24日的餐费）。

                    ### 食
                    - 主要消费内容
                    - 主要消费场所
                    - 最高消费价格
                    ### 衣
                    - 最高消费价格
                    - 主要消费品牌
                    ### 住
                    - 最高消费价格
                    - 主要消费场所
                    - 主要消费内容
                    ### 行
                    - 最高消费价格
                    ### 玩
                    - 最高消费价格
                    -主要消费品类
                """
        
        response = client.chat.completions.create(
            model = 'deepseek-chat',
            response_format={"type": "text"},
            max_tokens=4030,
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

        return response.choices[0].message.content