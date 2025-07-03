import config
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from app_control import open_app, play_pause_spotify
import time

# Give LLM clear instructions and action format
template = """
You are an expert in answering questions about a pizza restaurant.

You can also control these desktop apps: notepad, paint, spotify.

If the user asks you to open or play music with any of these apps, respond in this exact format:
ACTION: <app_name> <operation>

Examples:
ACTION: spotify play
ACTION: notepad open
ACTION: paint open

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""

model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def process_llm_response(llm_output: str):
    out_str = llm_output.strip()
    if out_str.startswith("ACTION:"):
        parts = out_str[len("ACTION:"):].strip().split(maxsplit=2)
        if len(parts) >= 2:
            app_name = parts[0].lower()
            operation = parts[1].lower()
            if app_name == "spotify" and operation == "play":
                open_app(app_name)
                time.sleep(6)  # Give Spotify time to launch and become focusable
                play_pause_spotify()
            elif operation == "open":
                open_app(app_name)
            else:
                print(f"Unknown or unsupported operation: {operation} for app: {app_name}")
        else:
            print("ERROR: Unrecognized ACTION format from LLM:", out_str)
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