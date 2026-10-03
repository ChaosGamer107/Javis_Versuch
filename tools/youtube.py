import webbrowser
from Tools.tool_registry import register_tool

def open_youtube():
    
    webbrowser.open("https://www.youtube.com")

register_tool(
    "open_youtube",
    "Öffnet Youtube im Browser",
    open_youtube
)