import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from career_agent.tool_registry import tool_definitions,tool_map


load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")

client = OpenAI(
    api_key = api_key,
    base_url = base_url
)


def run_agent(user_text):
    messages = [
        {
            "role":"system",#system：给模型规定任务和规则
            "content":
            "从用户需求中提取岗位查询参数,"
            "min_salary必须保留用户输入的数字，不得自动乘100、1000或进行薪资单位换算。"
            "让模型根据用户需求选择工具并提取参数,"
            "工具执行完成后根据工具结果给用户自然语言回答。"
            "字段必须包含city、min_salary、keyword"
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
        tools = tool_definitions,
    )

    #第一次LLM返回的结果
    message = response.choices[0].message
    tool_calls = message.tool_calls
    if not tool_calls:
        return message.content
   
    tool_call = tool_calls[0]
    tool_execution = execute_tool(tool_call)
    tool_ok = tool_execution["ok"]
    if tool_ok:
        tool_result_text = json.dumps(tool_execution["data"],ensure_ascii=False)
    else:
        return tool_execution["error"]
       

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
        tools=tool_definitions
    )
    final_text = final_response.choices[0].message.content


    return final_text

def execute_tool(tool_call):
    tool_name = tool_call.function.name
    tool_function = tool_map.get(tool_name)

    if not tool_function:
        return {
            "ok": False,
            "error": "未找到对应的工具"
        }

    #Tool 参数解析
    try:
        arguments = json.loads(tool_call.function.arguments)        
        tool_result = tool_function(**arguments)


    except json.JSONDecodeError:
        return {
            "ok":False,
            "error":"Tool 参数JSON解析失败"
        }

    except TypeError:
        return{
            "ok":False,
            "error":"Tool 参数和函数定义不匹配"
        }

    return {
        "ok":True,
        "data":tool_result
    }
        



if __name__ == "__main__":
    user_text = input("请输入你的需求：")
    final_output = run_agent(user_text)
    print(final_output)



    






