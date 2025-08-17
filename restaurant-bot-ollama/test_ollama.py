import requests

OLLAMA_URL = "http://localhost:11434"
try:
    response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
    print("Success:", response.status_code, response.json())
except Exception as e:
    print("Error:", e)

