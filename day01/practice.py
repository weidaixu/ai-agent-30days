import json

with open("jobs.json", "r", encoding="utf-8") as f:
    jobs_data = json.load(f)


def filter_jobs(min_salary, target_city):
    found = False

    for job in jobs_data:
        if job["salary"] >= min_salary and job["city"] == target_city:
            print(job["name"], job["salary"], job["city"])
            found = True

    if found == False:
        print("没有找到符合的岗位")


min_salary = int(input("请输入最低工资："))
target_city = input("请输入目标城市：")

filter_jobs(min_salary, target_city)   


def load_jobs():
    with open ("jobs.json","r",encoding="utf-8") as file :
        jobs = json.load(file)
    return jobs

jobs_data = load_jobs()
print(jobs_data)