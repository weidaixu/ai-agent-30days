import json

#导入json
def load_jobs():
    with open ("jobs.json","r",encoding="utf-8") as file :
        jobs = json.load(file)
    return jobs

jobs_data = load_jobs()

print("-----分界线-----")

#筛选岗位
def filter_job(jobs,city,min_salary,keyword):
    result=[]

    for job in jobs:
        if (
            (city == "" or job["city"] == city)
            and job["salary"] >= min_salary
            and (keyword == "" or keyword in job["name"])
            ):
            result.append(job)

    return result

city = input("请输入城市：")


salary_input = input("请输入薪资：")
if salary_input == "":
    min_salary = 0
else:
    min_salary = int(salary_input)

keyword = input("请输入岗位关键词：")
filtered_jobs = filter_job(jobs_data,city,min_salary,keyword)


#优化岗位输出
def show_jobs(jobs):
    if len(jobs)==0:
        print("没有找到合适的岗位")
    else:
        print(f"一共找到{len(filtered_jobs)}个岗位")

        for job in filtered_jobs:
                print("岗位",job["name"])
                print("城市",job["city"])
                print("薪资",job["salary"])
                print("-------------------")
        
show_jobs(filtered_jobs)



#计算平均薪资
def average_salary(jobs):
    if len(jobs)==0:
        return 0

    total_salary = 0

    for job in jobs:
        total_salary = total_salary + job["salary"]

    average = total_salary / len(jobs)

    return average

avg = average_salary(filtered_jobs)

print(f"平均薪资：{avg}元")