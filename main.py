import config
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from app_control import open_app, play_pause_spotify, send_telegram_message
import time
import re
import speech_recognition as sr

# Updated Template
template = """
You are an AI assistant that can answer questions and control desktop applications.

CAPABILITIES:
1. Answer pizza restaurant questions using provided reviews
2. Control desktop apps: notepad, paint, spotify
3. Send messages via Telegram (opens via Windows 11 Start menu)

IMPORTANT TECHNICAL NOTE - WINDOWS 11 SPECIFIC:
- Telegram is opened using Windows 11 Start menu (Win key → type "Apps:telegram" → Click at 546,348)
- Simple click-based approach with fixed coordinates
- 8 second wait after typing is CRITICAL for app results to load

FORMATTING RULES FOR TELEGRAM:

Use EXACTLY this format:
ACTION: telegram send ContactName "Your message here"

- Contact name: NO quotes (unless it has special characters)
- Message: ALWAYS in double quotes
- One space between contact and message

IMPORTANT: When user says 'Send "message" to Contact' or 'Explain "topic" to Contact':
- Convert it to: ACTION: telegram send Contact "message"
- Everything in quotes is the message
- Everything after "to" is the contact name

EXAMPLES:

User: "Send 'Hello friend' to John"
You: ACTION: telegram send John "Hello friend"

User: "Explain 'BODMAS' to Paazi GGITS"
You: ACTION: telegram send Paazi GGITS "BODMAS stands for Brackets, Orders, Division, Multiplication, Addition, and Subtraction. It's the order of operations in mathematics."

User: "Send 'How are you today?' to Sarah"
You: ACTION: telegram send Sarah "How are you today?"

User: "Tell Sarah about pizza" 
You: ACTION: telegram send Sarah "Pizza is an Italian dish consisting of a flat, round base of dough topped with tomato sauce, cheese, and various toppings."

For app controls:
ACTION: spotify play (uses exe path)
ACTION: notepad open (uses exe path)
ACTION: paint open (uses exe path)

TELEGRAM WINDOWS 11 SPECIFIC INFO:
- Opens via: Win key → wait 3s → type "telegram" → wait 8s → Click at (546, 348) → wait 15s
- Fixed click coordinates where Telegram app appears
- 8 second wait after typing prevents web results
- Contact search uses Ctrl+F
- Messages typed using keyboard automation (clipboard for >30 chars)

RULES:
- ONLY output ACTION: lines for commands
- When user says 'Send "X" to Y', output: ACTION: telegram send Y "X"
- When user says 'Explain "X" to Y', generate explanation and output: ACTION: telegram send Y "explanation"
- Don't add any text before or after ACTION: lines

Reviews: {reviews}
User request: {question}
"""

model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def get_voice_command():
    """Get voice input from user"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n🎤 Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            # Listen for audio
            audio = recognizer.listen(source, timeout=5)
            print("🔄 Processing speech...")
            
            # Convert speech to text
            text = recognizer.recognize_google(audio)
            print(f"✅ You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("❌ No speech detected")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

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
    print("="*50)
    print("AI DESKTOP ASSISTANT")
    print("="*50)
    
    while True:
        print("\n" + "-"*30)
        print("Choose input method:")
        print("1. Text mode")
        print("2. Voice mode")
        print("3. Exit")
        
        choice = input("\nSelect (1/2/3): ").strip()
        
        if choice == "1":
            # Text mode
            question = input("\nEnter your request: ")
            if question.lower() == "exit":
                break
                
        elif choice == "2":
            # Voice mode
            print("\n[VOICE MODE]")
            question = get_voice_command()
            if not question:
                continue
            if "exit" in question.lower():
                break
                
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
            continue
        
        # Process the command (voice or text)
        print("\n🤖 Processing...")
        reviews = retriever.invoke(question)
        result = chain.invoke({"reviews": reviews, "question": question})
        process_llm_response(str(result))