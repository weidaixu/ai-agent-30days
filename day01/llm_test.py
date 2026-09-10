import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")

client = OpenAI(
    api_key = api_key,
    base_url = base_url
)
question = input("请输入你想询问的问题：")

response = client.chat.completions.create(
    model = model,
    messages = [
        {
            "role":"user",
            "content":question
        }
    ]
)


print(response.choices[0].message.content)