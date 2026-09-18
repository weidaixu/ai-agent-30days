from pydantic import BaseModel,Field
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")

client = OpenAI(
    api_key = api_key,
    base_url = base_url
)

test_jd = """某科技公司招聘 AI Agent 开发实习生

工作地点：杭州
薪资：200-300元/天

岗位职责：
1. 参与大模型应用和 AI Agent 系统开发
2. 使用 Python 和 FastAPI 开发后端接口
3. 参与 LLM Tool Calling 功能开发

岗位要求：
1. 本科及以上学历
2. 熟悉 Python
3. 了解 FastAPI 和大模型 API
4. 每周至少实习4天，连续实习3个月以上

加分项：
1. 熟悉 LangGraph 者优先
2. 有 RAG 项目经验加分

工作时间：9:30-18:30"""

class JDAnalysis(BaseModel):
    company_name:str
    job_title:str
    city:str
    salary_range:str
    responsibilities:list[str]
    requirements:list[str]
    bonus_skills:list[str] = Field(default=list)
    work_hours:str
    internship_requirement:str

def analyze_jd(jd_text):
    messages = [
        {
            "role":"system",
            "content":
            """你负责分析招聘JD,
            提取岗位的关键信息,
            不要编造JD中没有的信息。
            只输出 JSON
            必须包含：
            company_name
            job_title
            city
            salary_range
            responsibilities
            requirements
            work_hours
            internship_requirement
            不要输出 JSON 之外的解释文字
            只输出合法JSON
            bonus_skills 专门提取“优先、加分、熟悉更佳”等内容，不要混入 requirements
            bonus_skills 必须始终返回。如果 JD 中没有加分项，返回空列表 []，不要省略字段。
            不要使用Markdown代码块，不要输出```json和```或其他额外文字
            internship_requirement 要保留原始具体要求，不要只输出“是/否”
            requirements 只提取学历、技能、经验等岗位要求，不要包含实习天数、实习月份等时间要求。
            internship_requirement 专门提取每周到岗天数、连续实习时长、到岗时间等实习要求。"""
                    
        },
        {
            "role":"user",
            "content":jd_text
        }
    ]


    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    result_text = response.choices[0].message.content
    cleaned_text = result_text.replace("```json","").replace("```","").strip()
    
    jd_dict = json.loads(cleaned_text)
    jd_result = JDAnalysis(**jd_dict)
    return jd_result



def format_jd_analysis(jd_result):
    responsibilities_text = "\n".join(jd_result.responsibilities)
    requirements_text = "\n".join(jd_result.requirements)

    if jd_result.bonus_skills:
        bonus_text = "\n".join(jd_result.bonus_skills)
        bonus_section = f"加分项:\n{bonus_text}"
    else:
        bonus_section = ""

    
    formatted_text = (
        f"公司：{jd_result.company_name}\n"
        f"岗位：{jd_result.job_title}\n"
        f"城市：{jd_result.city}\n"
        f"薪资：{jd_result.salary_range}\n"
        f"岗位职责：{responsibilities_text}\n"
        f"岗位要求：{requirements_text}\n"
        f"{bonus_section}\n"
        f"工作时间：{jd_result.work_hours}\n"
        f"实习要求：{jd_result.internship_requirement}\n"
    )
    return formatted_text



if __name__ == "__main__":
    result = analyze_jd(test_jd)
    formatted_result = format_jd_analysis(result)
    print(formatted_result)