import config
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from app_control import open_app, play_pause_spotify, send_telegram_message
import time
import re

# Improved template: includes messaging and app control
template = """
You are an expert at pizza restaurant questions, app launching, and sending messages.

You can:
- Answer pizza restaurant questions using reviews.
- Control these desktop apps: notepad, paint, spotify. Use ACTION: <app_name> <operation> format.
- Use Telegram to send messages.

If the user says "Explain <topic> to <contact>", generate an explanation and reply ONLY with:
ACTION: telegram send <contact> "<your generated explanation>"

If the user says "Send '<message>' to <contact>", reply ONLY with:
ACTION: telegram send <contact> "<message>"

IMPORTANT: Always put the message in double quotes after the contact name!

For app controls:
ACTION: spotify play
ACTION: notepad open
ACTION: paint open

Here are some relevant reviews: {reviews}
User request: {question}
"""

model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def process_llm_response(llm_output: str):
    out_str = llm_output.strip()
    print(f"\n[DEBUG] LLM Output: {out_str}\n")  # Debug print
    
    # More flexible regex for telegram actions
    telegram_patterns = [
        r'ACTION:\s*telegram\s+send\s+([^"\s]+(?:\s+[^"\s]+)*)\s+"([^"]+)"',  # Unquoted contact, quoted message
        r'ACTION:\s*telegram\s+send\s+"([^"]+)"\s+"([^"]+)"',  # Both quoted
        r'ACTION:\s*telegram\s+send\s+([^"\s]+(?:\s+[^"\s]+)*)\s+(.+)',  # Unquoted contact, rest is message
        r'ACTION:\s*telegram\s+send\s+"([^"]+)"\s+(.+)',  # Quoted contact, rest is message
    ]
    
    telegram_found = False
    for pattern in telegram_patterns:
        match = re.match(pattern, out_str, re.IGNORECASE | re.DOTALL)
        if match:
            contact, message = match.groups()
            contact = contact.strip().strip('"')
            message = message.strip().strip('"')
            print(f"[INFO] Parsed - Contact: '{contact}', Message: '{message}'")
            
            # Actually send the message
            success = send_telegram_message(contact, message)
            if not success:
                print("[ERROR] Failed to send Telegram message")
            telegram_found = True
            break
    
    if not telegram_found and out_str.lower().startswith("action:"):
        # Handle other app actions
        parts = out_str[len("ACTION:"):].strip().split(maxsplit=2)
        if len(parts) >= 2:
            app_name = parts[0].lower()
            operation = parts[1].lower()
            if app_name == "spotify" and operation == "play":
                open_app(app_name)
                time.sleep(10)  # More time for slow PC
                play_pause_spotify()
            elif operation == "open":
                open_app(app_name)
            else:
                print(f"Unknown operation: {operation} for app: {app_name}")
        else:
            print("ERROR: Unrecognized ACTION format:", out_str)
    elif not telegram_found:
        # Just print the response
        print(out_str)
    out_str = llm_output.strip()
    telegram_match = re.match(
        r'ACTION:\s*telegram\s+send\s+("?[\w\s]+"?)\s+(.+)', 
        out_str, 
        re.IGNORECASE
    )
    if telegram_match:
        contact_raw, message_raw = telegram_match.groups()
        contact = contact_raw.strip().strip('"')
        message = message_raw.strip().strip('"')
        print(f"[INFO] Sending to Telegram contact '{contact}': {message}")
        send_telegram_message(contact, message)
        return


    # -------- App Launching/Control --------
    if out_str.startswith("ACTION:"):
        # Format: ACTION: <app_name> <operation>
        parts = out_str[len("ACTION:"):].strip().split(maxsplit=2)
        if len(parts) >= 2:
            app_name = parts[0].lower()
            operation = parts[1].lower()
            if app_name == "spotify" and operation == "play":
                open_app(app_name)
                time.sleep(6)  # Give Spotify time to launch and be focusable
                play_pause_spotify()
            elif operation == "open":
                open_app(app_name)
            else:
                print(f"Unknown or unsupported operation: {operation} for app: {app_name}")
        else:
            print("ERROR: Unrecognized ACTION format from LLM:", out_str)
    else:
        # Show direct LLM answer
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