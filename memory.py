import json
import os

MEMORY_FILE = "data/memory.json"

def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_memory(memory):

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)

def remember(key, value, memory):

    memory[key] = value
    save_memory(memory)

def recall(key, memory):

    return memory.get(key)