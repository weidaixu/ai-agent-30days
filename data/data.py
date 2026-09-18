import json
#调用json
def load_jobs():
    with open("jobs.json","r",encoding = "utf-8") as file:
        jobs = json.load(file)

    return jobs