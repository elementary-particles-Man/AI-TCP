import requests
import json


def resume_session(session_id: str, old_pubkey: str):
    url = "http://127.0.0.1:8080/api/resume"
    headers = {"Content-Type": "application/json"}
    data = {"session_id": session_id, "old_pubkey": old_pubkey}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()
