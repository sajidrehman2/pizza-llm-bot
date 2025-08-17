# Restaurant Chatbot (100% Free) — Streamlit + Ollama

This project is **fully free**: runs locally with [Ollama](https://ollama.ai) and uses open models (e.g., Llama 3).
No API keys, no usage costs.

## 0) Requirements
- Windows/macOS/Linux
- Python 3.9+
- Ollama installed: https://ollama.ai
- (Optional) Cloudflare Tunnel to share publicly: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/

## 1) Install Ollama and a Model
Open PowerShell (Windows) or terminal (Mac/Linux):

```powershell
ollama --version          # should print a version; if not, install + restart PC
ollama pull llama3        # downloads the model
# (You can also pull: mistral, phi3)
```

> If `ollama` is not recognized, install it and restart your PC so PATH updates.

## 2) Create & Activate a Virtual Environment (Windows)
From the project folder:

```powershell
python -m venv venv
# If activation is blocked by execution policy, do ONE of the following:
.env\Scriptsctivate.bat                  # simplest
# or (temporary and safe for this terminal only):
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.env\Scriptsctivate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3) Install Python Dependencies
```bash
pip install -r requirements.txt
```

## 4) Run the App
Make sure you have pulled a model (e.g., `ollama pull llama3`). Then:

```bash
streamlit run app.py
```

Open the local URL (usually http://localhost:8501).

## 5) Use the App
- Chat to build an order.
- Press **“Summarize to JSON”** to get a structured order.
- The app uses **menu.json** to price items and writes line items to **orders.csv**.

## 6) Customize the Menu
Edit `menu.json` with your own items, sizes, and prices. The bot only offers items present in this file.

## 7) Troubleshooting
- **`ollama : not recognized`** → Install Ollama and restart PC; then run `ollama --version`.
- **Connection error to Ollama** → Ensure Ollama is running and model is pulled. Try `ollama pull llama3`.
- **JSON parsing failed** after summarize → Click Summarize again or clarify sizes/quantities in chat.
- **orders.csv not created** → You must summarize at least one order first.
- **Change server/port** → set env var `OLLAMA_URL` to override (default is `http://localhost:11434/api/chat`).

## 8) Make It Public (optional, free)
Use Cloudflare Tunnel:
```bash
cloudflared tunnel login
cloudflared tunnel --url http://localhost:8501
```
This gives you a public HTTPS URL while it runs.

---

All components are free: Streamlit, Requests, Pandas, and Ollama + open models.
