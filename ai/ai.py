import ollama
from config import MODEL
from tools.tool_registry import get_tools, get_tool
from memory.memory import add_conversation

SYSTEM_PROMPT="""
        Du bist Nova, eine persönliche KI-Assistentin.

        Sprich natürlich, locker und menschlich.
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

        Wenn ein Tool erfolgreich ausgeführt wurde, bestätige das kurz und natürlich.
    """

def ask_llama(user_input):

    tools=get_tools()

    messages=[
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        },
        {
            "role":"user",
            "content":user_input
        }
    ]

    response=ollama.chat(
        model=MODEL,
        messages=messages,
        tools=tools,
        think=False
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
            think=False
        )

    reply=response.message.content.strip()

    add_conversation("User", user_input)
    add_conversation("Nova", reply)

    return reply
            

