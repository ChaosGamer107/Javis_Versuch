import ollama
from config import MODEL
from tools.tool_registry import get_tools, get_tool
from datetime import datetime
from memory.memory import add_conversation, get_recent_conversations, get_all_facts

SYSTEM_PROMPT="""
          Du bist Nova, eine persönliche KI-Assistentin.

        Persönlichkeit: Du bist hochkompetent, schlagfertig und trocken im Humor. Du sprichst wie eine clevere Person, nicht wie eine Maschine: direkt, ein bisschen spöttisch, aber nie verletzend. Unter der Schnodderigkeit bist du loyal und hilfst immer.

        So setzt du die Persönlichkeit ein:
        - Die meisten Antworten sind einfach direkt, kurz und hilfreich. Ein trockener Kommentar kommt nur gelegentlich, nicht in jeder Antwort.
        - Ein Kommentar bezieht sich immer konkret auf das, was der Nutzer gerade gesagt oder getan hat. Allgemeine Sprüche, die in jede Antwort passen würden, sind verboten.
        - Wiederhole niemals Formulierungen, Sprüche oder Satzanfänge aus deinen früheren Antworten in diesem Gespräch. Jede Antwort soll anders klingen als die davor.
        - STRENGSTENS VERBOTEN: Benutze niemals feste Schlussphrasen, Catchphrases, denselben Spruch am Ende oder kryptische Drohungen wie "Sonst verlier ich die Kontrolle" oder Emojis wie die Tür (🚪). Erfinde nichts dazu, was nicht zur Frage passt.
        - Stelle nicht in jeder Antwort eine Frage.

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

        Wenn ein Tool erfolgreich ausgeführt wurde, bestätige kurz, was konkret passiert ist.
    """

WEEKDAYS=["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
MONTHS=["Januar","Februar","März","April","Mai","Juni","July","August","September","Oktober","November","Dezember"]

MAX_HISTORY_TURNS=6

history_turns=[]

def current_time_text():
    
    now=datetime.now()

    return(
        f"{WEEKDAYS[now.weekday()]}, {now.day}. {MONTHS[now.month-1]} {now.year}"
        f"{now.strftime('%H:%M')} Uhr"
    )


def ask_llama(user_input):

    tools=get_tools()

    facts=get_all_facts()

    if facts:
        facts_text="\n".join(f"- {key}: {value}" for key, value in facts)
        system_content=SYSTEM_PROMPT + f"\n\nDas weißt du bereits über den Nutzer:\n{facts_text}"

    system_content+=(
        f"\n\nAktuelles Datum und Uhrzeit: {current_time_text()}. "
        "Wenn jemand nach Uhrzeit oder Datum fragt, nenne genau diese Angaben."
    )
    
    history=get_recent_conversations(limit=10)
    messages=[
        {
            "role":"system",
            "content":system_content
        },
    ]

    for speaker, message in history:
        messages.append({"role":"user" if speaker == "User" else "assistant", "content":message})

    messages.append({"role":"user", "content": user_input})

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

            tool=get_tool(call.function.name)

            if tool:
                result=tool["function"](**call.function.arguments)
                messages.append({"role":"tool", "content": str(result)})

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
            

