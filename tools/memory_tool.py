from tools.tool_registry import register_tool
from memory.memory import save_fact

def remember_fact(key, value):
    """Speichert eine Information über den Nutzer dauerhaft im Langzeitgedächtnis.

    Args:
        key: Kurzes Stichwort für die Information, z.B. "Lieblingsfarbe" oder "beruf".
        value: Der zu speichernde Inhalt, z.B. "blau" oder "Student".
    """
    save_fact(key, value)
    return f"Gemerkt: {key} = {value}"

register_tool(
    "remember_fact",
    "Speicher eine Information über den Nutzer dauerhaft, wenn der Nutzer explizit darum bittet (z.B. 'merk dir, dass...').",
    remember_fact
)