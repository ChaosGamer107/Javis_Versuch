import webbrowser
from Tools.tool_registry import register_tool

def open_youtube():
    
    webbrowser.open("https://www.youtube.com")
    
    return "Ich öffne Youtube"

register_tool(
    "youtube",
    open_youtube,
    "Öffnet Youtube im Browser"
)