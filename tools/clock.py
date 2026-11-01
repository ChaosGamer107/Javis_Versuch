from datetime import datetime
from tools.tool_registry import register_tool

def get_time():

    print("TOOL Uhrzeit ausgeführt")
    
    return datetime.now().strftime("%H:%M:%S")


register_tool(
    "get_time",
    "Liefert die aktuelle lokale Uhrzeit.",
    get_time
)