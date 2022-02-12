import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE + "transaction/1", {"date": "2016-10-23", "description": "Netflix", "Amount": 20.99})
print(response.json())