import requests
import json


def send_secure_task(task_id: str, payload: str, session_key: str):
    url = "http://127.0.0.1:8080/api/secure"
    headers = {"Content-Type": "application/json"}
    data = {"task_id": task_id, "payload": payload, "session_key": session_key}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()
