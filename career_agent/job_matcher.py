from career_agent.candidate_profile import CandidateProfile
from pydantic import BaseModel
from career_agent.jd_analyzer import analyze_jd
from career_agent.resume_analyzer import analyze_resume

class MatchResult(BaseModel):
        matched_skills:list[str]
        missing_skills:list[str]

def match_skills(job_result,candidate):
    job_skills_set = set(job_result.required_skills)
    candidate_set = set(candidate.skills)
    matched_skills = job_skills_set & candidate_set
    missing_skills = job_skills_set - candidate_set

    result = MatchResult(
         matched_skills=list(matched_skills),
         missing_skills=list(missing_skills)
    )
    return result



if __name__ == "__main__":
    test_jd = """
    某科技公司招聘 AI Agent 开发实习生

    岗位要求：
    1. 熟悉 Python
    2. 熟悉 FastAPI
    3. 了解 Docker
    4. 有 RAG 项目经验

    加分项：
    熟悉 LangGraph

    每周至少实习4天，连续实习3个月以上
    """

    test_resume = """
    本科，智能科学与技术专业。

    项目：AI Career Agent
    使用 Python、FastAPI、Pydantic、LLM API 和 Tool Calling
    开发 AI 求职助手，完成 JD 结构化分析和岗位技能匹配。
    """
    jd_result = analyze_jd(test_jd)
    candidate = analyze_resume(test_resume)
    result = match_skills(jd_result, candidate)





    print(result)