# ARIA  
**Automated Responsive Intelligent Assistant**

ARIA is a desktop‐based AI assistant powered by LangChain and Ollama. It can fetch relevant restaurant reviews, control your desktop apps (Notepad, Paint, Spotify), automate Telegram messages, manage system functions (volume, lock, shutdown/restart), and drive your browser (Google, YouTube, any website) — all hands‑free.

---

## 🔍 Features

- **Natural‑language querying** over a local review database  
- **Voice & text modes**: talk or type your requests  
- **Desktop control**  
  - Open/close apps (Notepad, Paint, Spotify)  
  - Play/pause Spotify  
- **Telegram automation**  
  - Open chat, search by contact, send messages  
- **System commands**  
  - Volume up/down/mute  
  - Lock screen  
  - Schedule or cancel shutdown/restart  
- **Browser automation**  
  - Google or YouTube searches  
  - Open any URL  

---

## 📋 Prerequisites

1. **OS**: Windows 11  
2. **Python** ≥ 3.8  
3. **Ollama CLI** installed and running locally  
   - I’m using **llama3.1** for chat (fits my PC specs)  
   - You can pick any other Ollama model you prefer  
4. **Embedded‑model**  
   - I used `mxbai-embed-large`  
   - You’re free to swap in another embedding model  

---

## ⚙️ Installation

```bash
# 1. Clone this repo
git clone https://github.com/pranavv444/ai-local-agent.git aria
cd aria

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Prepare the vector database (first run)
python vector.py
