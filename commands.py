from datetime import datetime
import webbrowser

def get_time():
    now = datetime.now()
    print("DEBUG SYSTEM TIME:", now)
    return f"Es ist {now.strftime('%H:%M:%S')} Uhr"

def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Ich öffne Youtube"

if "erinnerst du dich" in user_input.lower():
    keyword=user_input.lower().replace(
        "erinnerst du dich",
        ""
    ).strip()

    memories=search_memories(keyword)

    if memories:
        result=memories[0][0]
    else:
        result="Dazu habe ich nichts gespeichert."

    print("Nova:", result)
    speak(result)
    

if "exit" in text or "beenden" in text or "stop" in text:
    print("Nova: Bis bald!")
    speak("Okay, ich fahre runter")
    break

    

if any(word in user_input.lower() for word in ["uhr","zeit","spät"]):
    result=get_time()
    print("Nova:",result)
    speak(result)
    
