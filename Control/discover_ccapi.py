import requests
import json

base = "http://172.20.10.2:8080/ccapi"

r = requests.get(base)

print("STATUS:", r.status_code)

data = r.json()

print(json.dumps(data, indent=4))