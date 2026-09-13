import requests


params = {
    "city":"福州",
    "salary":160
}


url = "https://httpbin.org/get"

response = requests.get(url,params = params)
print(response)
print(response.status_code)
print(type(response.text))
data = response.json()

print(type(data))
print(data)

args = data["args"]

print(args)
print(type(args))
print(args["city"])
print(args["salary"])

min_salary = int(args["salary"])

print(type(min_salary))