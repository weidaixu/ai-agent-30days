import json

#
def load_jobs():
    with open ("jobs.json","r",encoding = "utf-8") as file:
        jobs = json.load(file)
    return jobs
jobs_data = load_jobs()

print (jobs_data)

#岗位筛选
def filter_job(jobs,city,min_salary,keyword):
    result=[]

    for job in jobs:
        if (
            (city == "" or city == job["city"])
            and job["salary"] >= min_salary
            and (keyword == "" or keyword == job["name"])
            ):
            result.append(job)

    return result

city = input("请输入城市：")

salary_intput= input("请输入薪资：")
if salary_intput == "":
    min_salary = 0
else:
    min_salary = int(salary_intput)

keyword = input("请输入关键字：")

filtered_jobs = filter_job(jobs_data,city,min_salary,keyword)

#岗位输出
def show_jobs(jobs):
    if len(jobs) == 0:
        print("没有找到合适的岗位")
    else:
        print(f"一共找到{len(filtered_jobs)}个岗位")

        for job in filtered_jobs:
            print("岗位",job["name"])
            print("薪资",job["salary"])
            print("城市",job["city"])
            print("------------------")
show_jobs(filtered_jobs)

def average_salary(jobs):
    if len(jobs) == 0:
        return 0
    total_salary = 0

    for job in jobs:
        total_salary = total_salary + job["salary"]

    average = total_salary/len(job)
    return average
avg = average_salary(filtered_jobs)
print(f"平均薪资是{avg}")



