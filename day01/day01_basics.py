import json






name = "AI Agent实习生"
salary = 180
city = "福州"


print (name)
print (salary)
print (city)


jobs = [
    "AI Agent实习生",
    "Python后端实习生",
    "前端开发实习生",
    "Java开发实习生",
    "大模型应用开发实习生"
]

print (jobs)
print (jobs[0])
print (jobs[-1])


print ("------所有岗位------")

for job in jobs :
    print ("岗位：",job)


print ("-----AI/Python岗位-----")

for job in jobs :
    if "Python" in job or "AI" in job :
        print (job)



job = {
    "name": "AI Agent实习生",
    "salary": 180,
    "city": "福州"
}

print(job["name"])
print(job["salary"])
print(job["city"])

jobs_data = [
    {
        "name": "AI Agrnt实习生",
        "salary": 180,
        "city": "福州"

    },
    {
        "name": "Python后端实习生",
        "salary": 170,
        "city": "厦门"
    },
    {
        "name": "前端开发实习生",
        "salary": 150,
        "city": "泉州"
    }
]
for job in jobs_data:
    print(job["name"],job["salary"],job["city"])



print ("-----高薪职位-----")

for job in jobs_data:
    if job["salary"] > 170:
        print (job["name"],job["salary"],job["city"])





print("-----定义函数-----")
def filter_job(min_salary):
    for job in jobs_data:
        if job["salary"] >= min_salary:
            print (job["name"],job["salary"],job["city"])

     


with open("jobs.json", "r", encoding="utf-8") as f:
    jobs_data = json.load(f)

print(jobs_data)

min_salary = input ("请输入最低工资：")
print(min_salary)