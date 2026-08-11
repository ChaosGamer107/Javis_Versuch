from datetime import datetime
from tools.tool_registry import register_tool

def get_time():
    
    now = datetime.now()
    
    return f"Es ist {now.strftime('%H:%M:%S')} Uhr"


register_tool(
    "get_time",
    "Liefert die aktuelle lokale Uhrzeit.",
    get_time,
    parameters={}
)