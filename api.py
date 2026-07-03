import requests

API_KEY = "YOUR_KEY"

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "user", "content": "Say hello"}
        ]
    }
)

print(response.status_code)
print(response.text)