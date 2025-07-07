import config
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from app_control import open_app, play_pause_spotify, send_telegram_message
import time
import re

# Template is GOOD - keep it as is
template = """
You are an AI assistant that can answer questions and control desktop applications.

CAPABILITIES:
1. Answer pizza restaurant questions using provided reviews
2. Control desktop apps: notepad, paint, spotify
3. Send messages via Telegram (opens via Windows 11 Start menu)

IMPORTANT TECHNICAL NOTE - WINDOWS 11 SPECIFIC:
- Telegram is opened using Windows 11 Start menu (Win key → type "telegram" → Click)
- The system uses Start menu search with mouse click at fixed position (546, 348)
- NO Tab key (it goes to web section), NO Run dialog, NO exe paths
- Simple click-based approach for reliability
- Designed for slow PCs with appropriate delays

FORMATTING RULES FOR TELEGRAM:

Use EXACTLY this format:
ACTION: telegram send ContactName "Your message here"

- Contact name: NO quotes (unless it has special characters)
- Message: ALWAYS in double quotes
- One space between contact and message

EXAMPLES:

User: "Explain BODMAS to Paazi GGITS"
You: ACTION: telegram send Paazi GGITS "BODMAS stands for Brackets, Orders, Division, Multiplication, Addition, and Subtraction. It's the order of operations in mathematics."

User: "Send 'Hello friend' to John"
You: ACTION: telegram send John "Hello friend"

User: "Tell Sarah about pizza"
You: ACTION: telegram send Sarah "Pizza is an Italian dish consisting of a flat, round base of dough topped with tomato sauce, cheese, and various toppings."

For app controls:
ACTION: spotify play (uses exe path)
ACTION: notepad open (uses exe path)
ACTION: paint open (uses exe path)

TELEGRAM WINDOWS 11 SPECIFIC INFO:
- Opens via Windows 11 Start menu: Win key → wait 3s → type "telegram" → wait 3s → Click at (200, 150)
- Fixed click position where first app result appears in Windows 11
- NO Tab key usage (causes issues with web search)
- Contact search uses Ctrl+F in Telegram after 10 attempts to find window
- Messages typed using keyboard automation (clipboard for long messages >30 chars)
- Window focusing includes multiple mouse clicks for reliability
- Delays: 3s after Win key, 3s after typing, 15s for app to open, 5s between window checks

RULES:
- ONLY output ACTION: lines for commands
- For explanations, generate the full explanation and put it in quotes
- For simple messages, just forward the message in quotes
- Don't add any text before or after ACTION: lines

Reviews: {reviews}
User request: {question}
"""

model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def process_llm_response(llm_output: str):
    out_str = llm_output.strip()
    print(f"\n[DEBUG] LLM Output: {out_str}\n")  # Debug print
    
    # Check if it's an ACTION command
    if out_str.upper().startswith("ACTION:"):
        # Extract the action part after "ACTION:"
        action_part = out_str[7:].strip()  # Skip "ACTION:" (7 chars)
        
        # Check if it's a telegram command
        if action_part.lower().startswith("telegram send"):
            # Extract everything after "telegram send"
            telegram_part = action_part[13:].strip()  # Skip "telegram send" (13 chars)
            
            # Try different patterns to parse contact and message
            telegram_patterns = [
                # Pattern 1: Contact without quotes, message with quotes
                r'^([^"]+?)\s+"([^"]+)"$',
                # Pattern 2: Both with quotes
                r'^"([^"]+)"\s+"([^"]+)"$',
                # Pattern 3: Contact without quotes, message without quotes (fallback)
                r'^(\S+(?:\s+\S+)*?)\s+(.+)$'
            ]
            
            matched = False
            for pattern in telegram_patterns:
                match = re.match(pattern, telegram_part)
                if match:
                    contact, message = match.groups()
                    contact = contact.strip()
                    message = message.strip()
                    
                    print(f"[INFO] Parsed telegram command:")
                    print(f"       Contact: '{contact}'")
                    print(f"       Message: '{message}'")
                    
                    # Send the message
                    success = send_telegram_message(contact, message)
                    if not success:
                        print("[ERROR] Failed to send Telegram message")
                    matched = True
                    break
            
            if not matched:
                print(f"[ERROR] Could not parse telegram command: {telegram_part}")
        
        # Check if it's another app command (spotify, notepad, paint)
        else:
            parts = action_part.split(maxsplit=1)
            if len(parts) >= 2:
                app_name = parts[0].lower()
                operation = parts[1].lower()
                
                if app_name == "spotify" and operation == "play":
                    open_app(app_name)
                    time.sleep(10)  # Extra time for slow PC
                    play_pause_spotify()
                elif operation == "open" and app_name in ["notepad", "paint"]:
                    open_app(app_name)
                else:
                    print(f"Unknown operation: {operation} for app: {app_name}")
            else:
                print(f"[ERROR] Invalid action format: {action_part}")
    
    # If not an ACTION, just print the response
    else:
        print(out_str)

if __name__ == "__main__":
    while True:
        print("\n\n-------------")
        question = input("Ask your question (q to quit): ")
        print("\n\n")
        if question.lower() == "q":
            break
        reviews = retriever.invoke(question)
        result = chain.invoke({"reviews": reviews, "question": question})
        process_llm_response(str(result))