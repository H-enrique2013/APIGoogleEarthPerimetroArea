import json

with open("service-account.json", "r") as f:
    content = f.read()

print(json.dumps(content))

