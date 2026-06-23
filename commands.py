from datetime import datetime
import webbrowser

def get_time():
    now = datetime.now()
    print("DEBUG SYSTEM TIME:", now)
    return f"Es ist {now.strftime('%H:%M:%S')} Uhr"

def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Ich öffne Youtube"
