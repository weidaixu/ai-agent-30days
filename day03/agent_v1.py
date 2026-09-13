import json


#调用json
def load_jobs():
    with open("jobs.json","r",encoding = "utf-8") as file:
        jobs = json.load(file)

    return jobs

#岗位筛选
def filter_job(jobs,city,min_salary,keyword):
    result = []

    for job in jobs:
        if(
            (city == "" or city == job["city"])
            and job["salary"] >= min_salary
            and (keyword == "" or keyword in job["name"])
        ):
            result.append(job)

    return result



#岗位查询
def search_job_tool(city,min_salary,keyword):
    jobs = load_jobs()

    result = filter_job(jobs,city,min_salary,keyword)

    for job in result:
        print(job["name"],job["city"],job["salary"])

    return result



#城市筛选
def filter_city_jobs(jobs,city):
    result = []

    for job in jobs:
        if city == "" or job["city"] == city:
            result.append(job)

    return result


#平均薪资
def average_salary_tool(jobs):
    if len(jobs) == 0:
        print("没有符合条件的岗位")
        return
    
    total_salary = 0

    for job in jobs:
        total_salary = total_salary + job["salary"]

    average_salary = total_salary/len(jobs)
    print(f"平均工资是{average_salary}")




#城市岗位平均薪资
def city_average_salary_tool():
    jobs = load_jobs()

    city = input("请输入城市：")

    filtered_jobs = filter_city_jobs(jobs,city)

    average_salary_tool(filtered_jobs)



#查询城市最高薪资
def city_highest_salary_tool():
    jobs = load_jobs()

    city = input("请输入城市：")

    filtered_jobs = filter_city_jobs(jobs,city)

    if len(filtered_jobs) == 0:
        print("没有合适的岗位")
        return

    highest_job = filtered_jobs [0]

    for job in filtered_jobs:
        if job["salary"] > highest_job["salary"]:
            highest_job = job

    print(f"最高薪资岗位：{highest_job["name"]}")
    print(f"城市：{highest_job["city"]}")
    print(f"最高薪资:{highest_job["salary"]}")

#Agent
def agent(user_text):
    if "最高薪资" in user_text:
        city_highest_salary_tool()

    elif "平均薪资" in user_text:
        city_average_salary_tool()

    elif "岗位" in user_text or "工作" in user_text:
        search_job_tool("福州", 160, "AI")

    else:
        print("我暂时不知道该调用什么工具")


#用户输入
if __name__ == "_main_":
    user_text = input("请输入你的需求：")
    agent(user_text)

