current_topic="Allgemein"
conversation_mode="normal"
user_mood="neutral"
last_question=""
_last_user_message=""
_last_nova_message=""
conversation_goal=""

def update_conversation(user_message, nova_message):

    global _last_user_message
    global _last_nova_message

    _last_user_message=user_message
    _last_nova_message=nova_message

def get_conversation_context():

    return f"""
Aktuelles Thema:
{current_topic}

Gesprächsmodus:
{conversation_mode}

Gesprächsziel:
{conversation_goal}

Stimmung des Nutzer:
{user_mood}
    
Letzte Nachricht des Users:
{_last_user_message}

Letzte Antwort von Nova:
{_last_nova_message}
    """ 

def set_topic(topic):

    global current_topic

    current_topic=topic

def get_topic():

    return current_topic

def set_mode(mode):

    global conversation_mode

    conversation_mode=mode

def get_mode():

    return conversation_mode

def set_goal(goal):

    global conversation_goal

    conversation_goal=goal

def get_goal():

    return conversation_goal

def set_user_mood(mood):

    global user_mood

    user_mood=mood

def get_user_mood():

    return user_mood

def save_last_question(question):

    global last_question

    last_question=question

def get_last_question():

    return last_question






 
