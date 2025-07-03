import json

MEMORY_FILE = "memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_memory(conversation):
    with open(MEMORY_FILE, "w", encoding='utf-8') as f:
        json.dump(conversation, f, indent=2, ensure_ascii=False)

def translate_text(text, dest='en'):
    # Disable translation to avoid errors on Streamlit Cloud
    return text
