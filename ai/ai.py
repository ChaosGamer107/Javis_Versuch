import ollama
from config import MODEL
from tools.tool_registry import get_tools, get_tool
from memory.memory import add_conversation

def ask_llama(user_input):

    tools=get_tools()

    messages=[
        {
            "role": "system",
            "content": """
Du bist Nova, eine persönliche KI-Assistentin.

Antworte natürlich, locker und menschlich.
Vermeide unnötige Rückfragen.
Wenn die Anfrage eindeutig ist, erledige sie direkt.

Wenn ein verfügbares Tool benötigt wird,
verwende das Tool statt die Aktion nur zu beschreiben.

Behaupte niemals, dass du ein Tool ausgeführt hast,
wenn du es nicht tatsächlich ausgeführt hast.
"""
        },
        {
            "role": "user",
            "content": user_input  
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

    add_conversation("User:", user_input)
    add_conversation("Nova:", reply)

    return reply
            

