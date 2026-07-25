from memory import get_all_facts

def select_memory(user_input):

    text=user_input.lower()

    selected=[]

    for key, value in get_all_facts():

        if "name" in text and "name" in key:
            selected.append((key, value))

        elif "wohn" in text and "wohn" in key:
            selected.append((key, value))

        elif "spiel" in text and "spiel" in key:
            selected.append((key, value))

        elif "farbe" in text and "farbe" in key:
            selected.append((key, value))

    return selected