from day03.data import load_jobs


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



#城市平均薪资
def city_average_salary_tool(city):
    jobs = load_jobs()
    city_jobs = []
    for job in jobs:
        if (city =="" or city == job["city"]):
            city_jobs.append(job)

    total_salary = 0
    for job in city_jobs:
        total_salary = total_salary + job["salary"]
    if len(city_jobs) == 0:
        print("没有查询到您所选城市的岗位")
        return
    else:
        average_salary = total_salary/len(city_jobs)
    return average_salary


#岗位查询工具
def search_job_tool(city,min_salary,keyword):
    jobs = load_jobs()

    result = filter_job(jobs,city,min_salary,keyword)

    return result





