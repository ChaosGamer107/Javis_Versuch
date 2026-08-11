import webbrowser
from tools.tool_registry import register_tool

def open_youtube():
    
    webbrowser.open("https://www.youtube.com")
    
    return "Ich öffne Youtube"

register_tool(
    "open_youtube",
    "Öffnet Youtube im Browser",
    open_youtube,
    parameters={}
)