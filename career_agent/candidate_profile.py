from pydantic import BaseModel

class CandidateProfile(BaseModel):
    skills:list[str]
    projects:list[str]
    education:str
    major:str
    available_duration:str


candidate = CandidateProfile(
    skills=[
        "Python",
        "FastAPI",
        "LLM API",
        "Tool Calling",
        "Pydantic",
        "JSON"
    ],
    projects=[
        "AI Career Agent"
    ],
    education="本科",
    major="智能科学与技术",
    available_duration="可连续实习3个月以上，每周可到岗5天"
)




job_skills = ["Python","RAG","FastAPI","JSON","react"]
job_skills_set = set(job_skills)
candidateProfile_skill_set = set(candidate.skills)
missing_skills = job_skills_set - candidateProfile_skill_set
matched_skills = job_skills_set & candidateProfile_skill_set





if __name__=="__main__":


    print(missing_skills)
    print(matched_skills)