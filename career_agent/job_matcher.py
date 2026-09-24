from career_agent.candidate_profile import CandidateProfile
from pydantic import BaseModel
from career_agent.jd_analyzer import analyze_jd,client,model
from career_agent.resume_analyzer import analyze_resume
from career_agent.llm_out_parser import parse_llm_json




class RequirementMatch(BaseModel):
    requirement:str
    status:str
    evidence:str
    reason:str



class MatchResult(BaseModel):
        matched_skills:list[str]
        not_found_skills:list[str]
        requirement_matches:list[RequirementMatch]



def match_skills(job_result,candidate):
    job_skills_set = set(job_result.required_skills)
    candidate_set = set(candidate.skills)
    matched_skills = job_skills_set & candidate_set
    not_found_skills = job_skills_set - candidate_set

    result = MatchResult(
         matched_skills=list(matched_skills),
         not_found_skills=list(not_found_skills),
         requirement_matches=[]
    )
    return result

def match_requirement(requirement, candidate):
        candidate_text = (
        f"技能：{candidate.skills}\n"
        f"项目：{candidate.projects}\n"
        f"学历：{candidate.education}\n"
        f"专业：{candidate.major}\n"
        f"可实习时间：{candidate.available_duration}\n"

        )

        messages = [
            {
                "role": "system",
                "content": """
        你是 AI Career Agent 中的岗位要求匹配模块。

        你的任务是：

        根据一条岗位要求和候选人的真实资料，
        判断候选人当前是否能够满足这条岗位要求。

        你只能根据提供的候选人资料进行判断，
        不能使用常识补充候选人没有提供的经历，
        不能编造技能、项目、学历或实习经历。

        status 只能是以下三个值之一：

        "matched"
        "missing"
        "uncertain"


        判断规则：

        1. matched

        只有候选人资料中存在明确证据，
        能够直接或通过合理的语义关系证明满足岗位要求时，
        才可以返回 matched。

        例如：

        岗位要求：
        有 Web 后端开发经验

        候选人资料：
        使用 FastAPI 开发后端 HTTP API

        可以判断为 matched。


        2. missing

        只有候选人资料中存在明确证据，
        能够证明候选人不满足岗位要求时，
        才可以返回 missing。

        例如：

        岗位要求：
        本科及以上学历

        候选人学历：
        大专

        可以判断为 missing。


        3. uncertain

        如果当前候选人资料不足以证明满足，
        同时也没有证据证明不满足，
        必须返回 uncertain。

        特别注意：

        候选人资料中“没有提到某项技能或经历”
        不能单独作为 missing 的依据。

        例如：

        岗位要求：
        熟悉 Docker

        候选人资料中没有出现 Docker

        应该返回 uncertain，
        不能返回 missing。


        evidence 规则：

        evidence 必须来自候选人提供的真实资料。

        不得编造不存在的经历。

        如果 status 为 matched，
        填写能够支持匹配判断的真实证据。

        如果 status 为 missing，
        填写能够证明不满足要求的真实证据。

        如果 status 为 uncertain，
        说明当前资料中缺少哪方面的明确证据。


        reason 规则：

        reason 用于解释为什么根据 evidence 得到当前 status。

        reason 可以进行合理的语义解释，
        但不能增加候选人资料中不存在的事实。


        只输出合法 JSON。

        必须包含以下三个字段：

        {
            "status": "matched | missing | uncertain",
            "evidence": "判断依据",
            "reason": "判断原因"
        }

        不要输出 Markdown。
        不要输出 ```json。
        不要输出 JSON 之外的任何解释文字。
        """
            },
            {
                "role": "user",
                "content": f"""
        岗位要求：
        {requirement}

        候选人资料：
        {candidate_text}
        """
            }
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages
        )

        result_text = response.choices[0].message.content
        result_dict = parse_llm_json(result_text)


        requirement_match = RequirementMatch(
            requirement=requirement,
            status=result_dict["status"],
            evidence=result_dict["evidence"],
            reason=result_dict["reason"]
        )
        return requirement_match



def match_education_requirement(require,candidate):

      
    education_levels = {
        "大专":1,
        "本科":2,
        "硕士":3,
        "博士":4
    }
    candidate_level = education_levels.get(candidate.education)
    required_level = 2

    if candidate_level is None:
        status = "uncertain"
        evidence = "候选人资料中没有明确学历信息"
        reason = "当前资料不足以判断候选人是否满足本科及以上学历要求"

    elif candidate_level >= required_level:
        status = "matched"
        evidence = f"学历：{candidate.education}"
        reason = "候选人学历达到岗位要求的本科及以上标准"

    else:
        status = "missing"
        evidence = f"学历：{candidate.education}"
        reason = "候选人学历低于岗位要求的本科及以上标准"


    education_match = RequirementMatch(
        requirement=require,
        status=status,
        evidence=evidence,
        reason=reason
    )

    return education_match



def match_single_requirement(requirement, candidate):
    if "本科" in requirement and "学历" in requirement:
        return match_education_requirement(requirement, candidate)

    return match_requirement(requirement, candidate)




def match_requirements(job_result, candidate):
    requirement_matches = []

    for requirement in job_result.requirements:
        match_result = match_single_requirement(
            requirement,
            candidate
        )
        requirement_matches.append(match_result)

    return requirement_matches



def match_job(job_result, candidate):
    skill_result = match_skills(job_result, candidate)
    requirement_matches = match_requirements(job_result, candidate)

    result = MatchResult(
        matched_skills=skill_result.matched_skills,
        not_found_skills=skill_result.not_found_skills,
        requirement_matches=requirement_matches
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
    result = match_job(jd_result, candidate)
    print(result)
