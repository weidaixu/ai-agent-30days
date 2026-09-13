import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from day03.agent_v1 import search_job_tool


load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")

client = OpenAI(
    api_key = api_key,
    base_url = base_url
)

schema = {
    "type":"object",
    "properties":{
        "city":{"type":"string"},
        "min_salary":{"type":"integer"},
        "keyword":{"type":"string"}
    },
       "required":[
        "city",
        "min_salary",
        "keyword"
    ]
}

tools = [
    {
        "type":"function",
        "function":{
            "name":"search_job_tool",
            "description":"根据城市、最低薪资和岗位关键词查询符合条件的岗位",
            "parameters":schema
        }
    }
]
def run_agent(user_text):
    messages = [
        {
            "role":"system",#system：给模型规定任务和规则
            "content":"从用户需求中提取岗位查询参数，让模型根据用户需求选择工具并提取参数，工具执行完成后根据工具结果给用户自然语言回答。字段必须包含city、min_salart、keyword"
        },
        {
            "role":"user",
            "content":user_text
        }
    ]
    #第一次LLM调用
    response = client.chat.completions.create(
        model = model,
        messages = messages,
        tools = tools,
        response_format={
            "type":"json_scheam",
            "json_schema":{
                "name":"job_search_params",
                "schema":schema,
                "strict":True
            }
        }
    )

    #第一次LLM返回的结果
    message = response.choices[0].message
    tool_call = message.tool_calls[0]

    #Tool 参数解析
    try:
        arguments = json.loads(tool_call.function.arguments)

        city = arguments["city"]
        min_salary = arguments["min_salary"]
        keyword = arguments["keyword"]

    except json.JSONDecodeError:
        print("Tool参数解析失败")
        return 

    except KeyError:
        print("Tool 参数确实必要的字段")
        return

    #执行Tool+把结果转成文本
    job_result = search_job_tool(city,min_salary,keyword)
    tool_result_text = json.dumps(job_result,ensure_ascii=False)    

    messages.append(message)  
    messages.append(
        {
            "role":"tool",
            "tool_call_id":tool_call.id,
            "content":tool_result_text
        }
    )
    #第二次调用LLM+输出最终答案
    final_response = client.chat.completions.create(
        model = model,
        messages=messages,
        tools=tools
    )
    final_text = final_response.choices[0].message.content
    return final_text

if __name__ == "__main__":
    user_text = input("请输入你的需求：")
    final_output = run_agent(user_text)
    print(final_output)



    






