from agent_v1 import search_job_tool


llm_result = {
    "city" : "福州",
    "min_salary" : 160,
    "keyword" : "AI"
}
city = llm_result["city"]
min_salary = llm_result["min_salary"]
keyword = llm_result["keyword"]


print(city)
print(min_salary)
print(keyword)
print("收到的最低薪资参数：",min_salary)

search_job_tool(city,min_salary,keyword)