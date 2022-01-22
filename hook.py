import json
import requests

# Easily send new webhooks to accommodate new users

with open('config.json') as json_file:
    config = json.load(json_file)

url = f"https://discord.com/api/webhooks/{config['webhookid']}/{config['webhooktoken']}" 
upload = "🍑"

r = requests.post(url, data={'content': upload})
print(r.status_code, " Success!")
