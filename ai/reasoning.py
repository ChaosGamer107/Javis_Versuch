from conversation import get_conversation_context
from memory import get_all_facts, get_recent_memories

def build_reasoning(user_input):

    facts=get_all_facts()
    memories=get_recent_memories()

    thought=[]

    thought.append("Interner Gedankengang:")
    thought.append("")

    thought.append("Gesprächskontext:")
    thought.append(get_conversation_context())

    thought.append("")

    if facts:
        thought.append("Bekannte Fakten:")

        for key, value in facts:
            thought.append(f"-{key}: {value}")

    thought.append("")

    if memories:
        thought.append("Relevante Erinnerungen:")

        for memory in memories:
            thought.append(f"-{memory[0]}")

    thought.append("")

    thought.append(f"Neue Nachricht des Nutzers: {user_input}")

    thought.append("")
    thought.append("Überlege:")

    thought.append("-Was möchte der Nutzer erreichen ?")
    thought.append("-Brauche ich ein Tool ?")
    thought.append("-Sollte ich Wissen aus dem Gedächtnis verwenden ?")
    thought.append("-Sollte ich eine Rückfrage stellen ?")
    thought.append("-Antworte natürlich")

    return "\n".join(thought)
