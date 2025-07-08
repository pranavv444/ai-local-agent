
# ARIA  
**Automated Responsive Intelligent Assistant**

ARIA is a desktop‑based AI assistant powered by LangChain and Ollama. It automates Telegram messaging, , controls apps (Notepad, Paint,  play songs on Spotify),fetches  restaurant reviews , manages system functions (volume, lock, shutdown/restart), and drives your browser (Google, YouTube, any site) — all hands‑free.

---

## 🔍 Features

- Natural‑language querying over a local review database  
- Voice & text modes: talk or type your requests  
- Desktop control:
  - Open/close apps (Notepad, Paint, Spotify)
  - Play/pause Spotify
- Telegram automation:
  - Open chat, search by contact, send messages
- System commands:
  - Volume up/down/mute
  - Lock screen
  - Schedule or cancel shutdown/restart
- Browser automation:
  - Google or YouTube searches
  - Open any URL

---

## 📋 Prerequisites

1. OS: Windows 11  
2. Python ≥ 3.8  
3. Ollama CLI installed and running locally  
   - Using llama3.1 (fits my PC specs) — feel free to pick another model
4. Embedding model
   - Using mxbai-embed-large — you can swap in another

---

## ⚙️ Configuration & Usage

1. **Clone the repo**:
   ```bash
   git clone https://github.com/pranavv444/ai-local-agent.git
   cd ai-local-agent


2. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Prepare vector database (first run only):

   ```bash
   python vector.py
   ```

5. Telemetry settings are in `config.py` (disabled by default):

   ```python
   import os
   os.environ["CHROMA_TELEMETRY"]      = "false"
   os.environ["ANONYMIZED_TELEMETRY"] = "false"
   ```

6. Model configuration:

   * Chat LLM (`main.py`):

     ```python
     model = OllamaLLM(model="llama3.1")
     ```
   * Embeddings (`vector.py`):

     ```python
     embeddings = OllamaEmbeddings(model="mxbai-embed-large")
     ```

7. Run ARIA:

   ```bash
   # Text mode
   python main.py
   # Choose "1" and type your request

   # Voice mode
   python main.py
   # Choose "2" and speak into your microphone

   # Exit
   # Choose "3" or type "exit"
   ```

**Examples:**

```
What highly rated pizza spots are near me?
Send "Hey, are we still on for tonight?" to Alice
Turn volume up
Search YouTube for "lofi hip hop"
```

---

## 📂 File Structure

```
├── app_control.py      # Windows app & system automation
├── config.py           # Telemetry settings
├── main.py             # Entry point & LLM orchestration
├── realistic_restaurant_reviews.csv
├── requirements.txt
├── vector.py           # Build/query local review embeddings
├── chrome_langchain_db # ChromaDB folder
└── .gitignore
```

---

## 🧰 Tech Stack

* Python (core logic)
* LangChain (agent orchestration)
* Ollama (LLM inference & embeddings)
* PyAutoGUI / Pynput (UI control)
* ChromaDB (local vector store)

---

## 🔭 Roadmap

1. **Dynamic Skill Generation**: Use the LLM to generate new skills on the fly.
2. **Vision‑Based UI Interaction**: Integrate a vision layer for screen parsing and decision making.
3. **Memory & Context**: Add long‑term memory for multi‑step workflows.
4. **Plugin Architecture**: Enable third‑party plugins and modular extensions.
5. **Enhanced Error Handling**: Build an evaluator/fixer loop for robust execution.
6. **Cross‑Platform Support**: Extend compatibility beyond Windows.

---

