import requests
import json
import time
import hashlib

URL = "http://localhost:1234/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}

# ログファイル名
LOG_FILE = "ping_loop_hash_log.txt"

# Ping回数
NUM_PINGS = 5

def sha256_hash(content: str) -> str:
    sha = hashlib.sha256()
    sha.update(content.encode('utf-8'))
    return sha.hexdigest()

def run_ping():
    payload = {
        "model": "google/gemma-3-4b",
        "messages": [
            {
                "role": "system",
                "content": "You are GeminiCLI communicating with google/gemma-3-4b via AI-TCP. Respond with simple confirmation."
            },
            {
                "role": "user",
                "content": "Ping test: Confirm connectivity and respond with a unique timestamp."
            }
        ],
        "temperature": 0.2,
        "stream": False
    }
    try:
        response = requests.post(URL, headers=HEADERS, data=json.dumps(payload))
        if response.status_code == 200:
            resp_json = response.json()
            # gemma-3-4bの返答だけ抜き出し
            timestamp_content = resp_json["choices"][0]["message"]["content"].strip()
            hash_value = sha256_hash(timestamp_content)
            log_entry = {
                "timestamp_content": timestamp_content,
                "hash": hash_value
            }
            print(f"✅ {log_entry}")
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        else:
            print(f"❌ Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    for i in range(NUM_PINGS):
        print(f"🔄 Ping with Hash #{i+1}")
        run_ping()
        time.sleep(2)
