import requests

url = "https://httpbin.org/post"

data = {
    "city": "福州",
    "salary": 160,
    "keyword": "AI"
}

response = requests.post(url,json = data)




print(response.status_code)

result = response.json()
result_json = result["json"]

print(result_json)
print(result_json["city"])
print(result_json["salary"])
print(type(result_json["salary"]))
print(result_json["keyword"])
