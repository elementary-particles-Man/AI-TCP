import requests
import json

url = "http://localhost:1234/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

payload = {
    "model": "google/gemma-3-4b",
    "messages": [
        {"role": "user", "content": "Explain the difference between supervised and unsupervised learning in one paragraph."}
    ],
    "temperature": 0.7,
    "stream": False
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print("Status Code:", response.status_code)
print("Response:", response.text)
