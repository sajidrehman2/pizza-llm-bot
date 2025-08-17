\
import requests, os, json
OLLAMA_URL = os.environ.get("OLLAMA_URL","http://localhost:11434/api/chat")
messages=[{"role":"system","content":"You are friendly."},{"role":"user","content":"Say hi in 5 words."}]
r = requests.post(OLLAMA_URL, json={"model":"llama3","messages":messages,"stream":False}, timeout=20)
print(r.status_code, r.text[:400])
