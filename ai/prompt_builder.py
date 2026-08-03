from personality import build_personality
from memory.conversation import get_conversation_context

def build_prompt(
        user_input,
        analysis,
        reasoning,
        plan,
        facts,
        context,
        conversation,
        tool_text
):

    fact_text=""

    for key, value in facts:
        fact_text_text+=f"{key}: {value}\n"

    context_text=""

    for item in context:
        context_text+=f"- {item}\n"

    conversation_text=""

    for speaker, message in conversation:
        conversation_text+=f"{speaker}: {message}\n"

    conversation_context=get_conversation_context

    prompt=f"""

    {build_personality()}

    Gesprächsanalyse:

    Gesprächsart:
    {analysis["type"]}

    Emotion:
    {analysis["emotion"]}

    Rückfrage stellen:
    {analysis["should_ask_question"]}

    Memory benutzen:
    {analysis["should_use_memory"]}

    Antwortlänge:
    {analysis["answer_length"]}

    Ziel:
    {analysis["goal"]}

    Interner Plan:

    Ziel:
    {plan["goal"]}

    Gesprächsart:
    {plan["conversation_type"]}

    Memory:
    {plan["use_memory"]}

    Tools:
    {plan["use_tools"]}

    Tool:
    {plan["tool"]}

    Thema fortführen:
    {plan["continue_topic"]}

    Rückfrage:
    {plan["ask_followup"]}

    {reasoning}

    {conversation_context}

    Bekannte Fakten:

    {fact_text}

    Relevante Informationen:

    {context_text}

    Letzte Unterhaltung:

    {conversation_text}

    Verfügbare Tools:

    {tool_text}

    User:

    {user_input}

    Nova:
        
        """

    return prompt