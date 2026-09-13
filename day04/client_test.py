import requests
url = "http://127.0.0.1:8000/chat"

data = {
    "message":"帮我找福州160以上的AI岗位"
}



response = requests.post(url,json = data)

result = response.json()

answer = result["answer"]
print(answer)