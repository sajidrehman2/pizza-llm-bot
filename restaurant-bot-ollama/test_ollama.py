# test_ollama.py
messages = [
    {"role": "system", "content": "You are friendly."},
    {"role": "user", "content": "Say hi in 5 words."}
]

# Use a mock response instead of localhost
r_status = 200
r_text = "Hello there! Have a great day."
print(r_status, r_text)

