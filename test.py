import requests

data = {
    "text": "Hi, urgently send your password now"
}

res = requests.post("http://127.0.0.1:5000/scan", json=data)
print(res.json())