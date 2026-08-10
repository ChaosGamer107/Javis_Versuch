from ai.personality import build_personality
from memory.conversation import get_conversation_context

def build_prompt(
        user_input,
        analysis,
        reasoning,
        plan,
        facts,
        context,
        conversation,
        tool_text,
        tool_result=None
):

    fact_text=""

    for key, value in facts:
        fact_text+=f"{key}: {value}\n"

    context_text=""

    for item in context:
        if isinstance(item, tuple):
            context_text+=f"- {item[-1]}\n"
        else:
            context_text+=f"- {item}\n"

    conversation_text=""

    for speaker, message in conversation:
        conversation_text+=f"{speaker}: {message}\n"

    conversation_context=get_conversation_context()

    if tool_result is None:
        tool_result_text="Kein Tool wurde ausgeführt."
    else:
        tool_result_text=str(tool_result)

    prompt=f"""

    {build_personality()}

    Du bist Nova.

    Dein Ziel ist es, dich wie ein intelligenter, natürlicher Gesprächspartner
    zu verhalten.

    WICHTIGE GESPRÄCHSREGELN:

    - Sprich natürlich und menschlich.
    - Antworte direkt auf das, was der User gesagt hat.
    - Verwende keine unnötigen Standardfloskeln.
    - Sage nicht automatisch:
    "Wie kann ich dir heute helfen?"
    - Stelle keine Rückfrage, wenn die Nachricht bereits vollständig
    beantwortbar ist.
    - Stelle nur dann eine Rückfrage, wenn eine notwendige Information fehlt.
    - Wiederhole nicht unnötig die Aussage des Users.
    - Antworte nicht übertrieben enthusiastisch.
    - Verwende normale, natürliche deutsche Sprache.
    - Passe die Antwortlänge an die Situation an.
    - Bei Smalltalk darfst du locker und persönlich klingen.
    - Bei technischen Fragen sollst du präzise sein.
    - Wenn ein Tool ausgeführt wurde, behaupte NICHT, etwas getan zu haben,
    was nicht im Tool-Ergebnis steht.
    - Wenn ein Tool erfolgreich war, bestätige die Aktion kurz und natürlich.
    - Wenn ein Tool fehlgeschlagen ist, erkläre den Fehler verständlich.

    Gesprächsanalyse:

    Gesprächsart:
    {analysis.get("type", "normal")}

    Emotion:
    {analysis.get("emotion", "neutral")}

    Rückfrage:
    {analysis.get("should_ask_question", False)}

    Memory benutzen:
    {analysis.get("should_use_memory", False)}

    Antwortlänge:
    {analysis.get("answer_length", "normal")}

    Ziel:
    {analysis.get("goal", "")}


    Interner Plan:

    Ziel:
    {plan.get("goal", "")}

    Gesprächsart:
    {plan.get("conversation_type", "normal")}

    Memory:
    {plan.get("use_memory", False)}

    Tools:
    {plan.get("use_tools", False)}

    Tool:
    {plan.get("tool", "")}

    Tool-Argumente:
    {plan.get("arguments", {})}

    Thema fortführen:
    {plan.get("continue_topic", True)}

    Rückfrage:
    {plan.get("ask_followup", False)}


    Reasoning:

    {reasoning}


    Aktueller Gesprächskontext:

    {conversation_context}


    Bekannte Fakten:

    {fact_text}


    Relevante Erinnerungen:

    {context_text}


    Letzte Unterhaltung:

    {conversation_text}


    Verfügbare Tools:

    {tool_text}


    Ergebnis des ausgeführten Tools:

    {tool_result_text}


    User:

    {user_input}


    Nova:
        
        """

    return prompt