import requests
import json
import time

URL = "http://localhost:1234/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}

# 保存するログファイル
LOG_FILE = "ping_loop_log.txt"

# 何回Pingするか
NUM_PINGS = 5

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
            print(f"✅ Response: {resp_json}")
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(resp_json, ensure_ascii=False) + "\n")
        else:
            print(f"❌ Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    for i in range(NUM_PINGS):
        print(f"🔄 Ping #{i+1}")
        run_ping()
        time.sleep(2)  # 2秒待機（必要に応じて調整）
