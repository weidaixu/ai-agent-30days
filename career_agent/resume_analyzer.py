import os

from dotenv import load_dotenv
from openai import OpenAI

from career_agent.candidate_profile import CandidateProfile

from career_agent.llm_out_parser import parse_llm_json

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def analyze_resume(resume_text):
    messages = [
        {
            "role":"system",
            "content":
            """
            你是一名资深的简历分析专家，你负责提取简历中存在的信息，不允许推测，
            必须输出："skills"、"projects"、"education"、"major"、available_duration"这五个字段。
            类型必须满足：skills → list[str]、projects → list[str]、education → str、major → str、available_duration → str
            skills 只提取明确出现或明确体现的技术能力，不要强行加入学习能力强、认真负责等主观内容
            project保存项目名称+简短真实技术描述，但不能添加简历里没有的技术,不要因为项目类型、岗位名称或常识推断简历未明确体现的技能。
            简历没写的东西不要编造，对于education、major、available_duration不存在返回""
            对于skills、projects不存在就返回[]
            只输出合法json，不要输出'''json等
            """
        },
        {
            "role":"user",
            "content": resume_text
        }
    ]

    response = client.chat.completions.create(
        model = model,
        messages = messages,
    )

    result_text = response.choices[0].message.content
    profile_dict = parse_llm_json(result_text)
    candidate_profile = CandidateProfile(**profile_dict)
    return candidate_profile


if __name__ == "__main__":
    test_resume = """
    本科，智能科学与技术专业。

    项目：AI Career Agent
    使用 Python、FastAPI、Pydantic、LLM API 和 Tool Calling
    开发 AI 求职助手，完成 JD 结构化分析和岗位技能匹配。
    """
    candidata = analyze_resume(test_resume)
    print(candidata)

    