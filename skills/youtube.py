import webbrowser
from apps.tool_registry import register_tool

def open_youtube():
    
    webbrowser.open("https://www.youtube.com")
    
    return "Ich öffne Youtube"

register_tool(
    name="youtube",
    description="Öffnet YouTube im Browser.",
    parameters=[],
    function=open_youtube
)