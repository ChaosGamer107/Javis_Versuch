curren_topic="Allgemein"
conversation_mode="normal"
user_mood="neutral"

last_question=""
last_user_message=""
conversation_goal=""

def analyze_conversations(user_input):

    global curren_topic
    global conversation_mode
    global last_user_message
    global conversation_goal

    text=user_input.lower()

    if any(word in text for word in [
        "python",
        "code",
        "programm",
        "programmieren",
        "fehler",
        "bug",
        "nova"
    ]):
        curren_topic="Programmieren"
        conversation_mode="coding"

    elif any (word in text for word in [
        "erkläre",
        "was ist",
        "warum",
        "wie funktioniert"
    ]):
        curren_topic="Lernen"
        conversation_mode="teaching"

    elif any(word in text for word in [
        "wie gehts",
        "hallo",
        "hi",
        "na"
    ]):
        curren_topic="Smalltalk"
        conversation_mode="chat"

    else:
        conversation_mode="normal"

def save_last_question(question):
    global last_question
    last_question=question

def get_conversation_context():

    return f"""
Aktuelles Thema:
{curren_topic}

Gesprächmodus:
{conversation_mode}

Stimmung:
{user_mood}

Letzte Nachricht:
{last_user_message}

Letzte Frage von Nova:
{last_question}
    """ 
