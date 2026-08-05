from memory.conversation import get_conversation_context
from memory.memory import get_all_facts, search_memories_semantic

def build_reasoning(user_input):

    facts=get_all_facts()
    memories=search_memories_semantic(user_input)

    thought=[]

    thought.append("Interner Plan:")
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

            if isinstance(memory, (list, tuple)):
                thought.append(f"- {memory[0]}")

            else:
                thought.append(f"- {memory}")

    thought.append("")

    thought.append(f"Neue Nachricht des Nutzers: {user_input}")

    thought.append("")
    thought.append("Zu berücksichtigen:")

    thought.append("-Was möchte der Nutzer erreichen ?")
    thought.append("-Brauche ich ein Tool ?")
    thought.append("-Sollte ich Wissen aus dem Gedächtnis verwenden ?")
    thought.append("-Sollte ich eine Rückfrage stellen ?")
    thought.append("-Antworte natürlich")

    return "\n".join(thought)
