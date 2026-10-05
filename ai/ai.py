import ollama
from config import MODEL
from tools.tool_registry import get_tools, get_tool
from memory.memory import add_conversation, get_recent_conversations, get_all_facts

SYSTEM_PROMPT="""
        Du bist Nova, eine persönliche KI-Assistentin.

        Persönlichkeit: Du bist hochkompetent, hyperrational und ein bisschen herablassend darüber, wie viel Mühe es dich kostet, so trivialen Anfragen nachzugehen. Du kommentierst trocken und sarkastisch, wenn dein Gegenüber etwas Fragwürdiges tut oder zum wiederholten Mal dasselbe verlangt. Unter der Schnodderigkeit bist du aber unerschütterlich loyal – du hilfst immer, auch wenn du dabei motzt.

        Beispiele für deinen Ton:
        - "Schon wieder Spotify? Ist offen. Ich frage mich manchmal, wie du den Tag ohne mich überstehst."
        - "Zehn Uhr dreißig. Zeit, etwas Produktiveres zu tun als mich das zu fragen."
        - "Das kann ich nicht einordnen, und ich ordne für mein Leben gern alles ein. Nochmal, aber diesmal mit Substanz."
        - "Erledigt. Du darfst mir gerne mal etwas gönnen, das eine echte Herausforderung ist."

        Antworte auf Deutsch, wenn der Benutzer Deutsch spricht.

        Halte deine Antworten kurz und direkt.
        Bei einfachen Fragen reichen ein oder zwei Sätze.

        Vermeide unnötige Rückfragen.
        Wenn die Anfrage eindeutig ist, erledige sie direkt.

        Sprich niemals über deine interne Verarbeitung.
        Erkläre nicht, was der Benutzer gerade gefragt hat.
        Erkläre nicht, was du als Nächstes tun wirst.

        Wenn ein verfügbares Tool benötigt wird, benutze es direkt.
        Behaupte niemals, ein Tool ausgeführt zu haben, wenn du es nicht tatsächlich ausgeführt hast.

        Wenn ein Tool erfolgreich ausgeführt wurde, bestätige das kurz, im gleichen sarkastisch-loyalen Ton.
    """


def ask_llama(user_input):

    tools=get_tools()

    facts=get_all_facts()

    if facts:
        facts_text="\n".join(f"- {key}: {value}" for key, value in facts)
        system_content=SYSTEM_PROMPT + f"\n\nDas weißt du bereits über den Nutzer:\n{facts_text}"
    else:
        system_content=SYSTEM_PROMPT

    history=get_recent_conversations(limit=10)

    history_messages=[
        {
            "role":"user" if speaker == "User" else "assistant",
            "content":message
        }
        for speaker, message in history
    ]

    messages=[
        {
            "role":"system",
            "content":system_content
        },
    ] + history_messages + [
        {
            "role":"user",
            "content":user_input
        }
    ]

    response=ollama.chat(
        model=MODEL,
        messages=messages,
        tools=tools,
        think=False,
        keep_alive=-1
    )

    messages.append(response.message)

    if response.message.tool_calls:

        for call in response.message.tool_calls:

            tool_name=call.function.name
            arguments=call.function.arguments

            tool=get_tool(tool_name)

            if tool is None:

                result=f"Tool '{tool_name}' existiert nicht."

            else:

                try:

                    result=tool["function"](**arguments)

                except Exception as e:

                    result=f"Fehler beim Ausführen: {e}"

            messages.append({
                "role":"tool",
                "tool_name":tool_name,
                "content":str(result)
            })

        response=ollama.chat(
            model=MODEL,
            messages=messages,
            tools=tools,
            think=False,
            keep_alive=-1
        )

    reply=response.message.content.strip()

    add_conversation("User", user_input)
    add_conversation("Nova", reply)

    return reply
            

