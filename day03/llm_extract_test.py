import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from day03.tools import search_job_tool,tool_map


load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")

client = OpenAI(
    api_key = api_key,
    base_url = base_url
)

search_job_schema = {
    "type":"object",
    "properties":{
        "city":{"type":"string"},
        "min_salary":{
            "type":"integer",
            "description":"最低薪资，必须直接使用用户输入的整数，不进行单位换算。"
            "例如用户输入160，则返回160。"
            },
        "keyword":{"type":"string"}
    },
       "required":[
        "city",
        "min_salary",
        "keyword"
    ]
}


city_average_salary_schema = {
    "type":"object",
    "properties":{
        "city":{
            "type":"string",
            "description":"要查询平均薪资的城市名字"
        },
    },
        "required":[
            "city"
        ]
}

tools = [
    {
        "type":"function",
        "function":{
            "name":"search_job_tool",
            "description":"根据城市、最低薪资和岗位关键词查询符合条件的岗位",
            "parameters":search_job_schema
        }
    },
        {
            "type":"function",
            "function":{
                "name":"city_average_salary_tool",
                "description":"查询指定城市岗位的平均薪资",
                "parameters":city_average_salary_schema
            }
        }
]
def run_agent(user_text):
    messages = [
        {
            "role":"system",#system：给模型规定任务和规则
            "content":
            "从用户需求中提取岗位查询参数,"
            "min_salary必须保留用户输入的数字，不得自动乘100、1000或进行薪资单位换算。"
            "让模型根据用户需求选择工具并提取参数,"
            "工具执行完成后根据工具结果给用户自然语言回答。"
            "字段必须包含city、min_salart、keyword"
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
    )

    #第一次LLM返回的结果
    message = response.choices[0].message
    tool_calls = message.tool_calls
    if not tool_calls:
        return message.content
   
    tool_call = tool_calls[0]
    tool_name = tool_call.function.name
    tool_function = tool_map.get(tool_name)

    if not tool_function:
        print("未找到工具")
        return

    #Tool 参数解析
    try:
        arguments = json.loads(tool_call.function.arguments)

    except json.JSONDecodeError:
        print("Tool参数解析失败")
        return 

    except KeyError:
        print("Tool 参数确实必要的字段")
        return
    #执行Tool+把结果转成文本
    tool_result = tool_function(**arguments)
    tool_result_text = json.dumps(tool_result,ensure_ascii=False)    

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



    print(tool_name)
    print(tool_function)

    return final_text





if __name__ == "__main__":
    user_text = input("请输入你的需求：")
    final_output = run_agent(user_text)
    print(final_output)



    






