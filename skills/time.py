from datetime import datetime
from tools.tool_registry import register_tool

def get_time():
    
    now = datetime.now()
    
    return f"Es ist {now.strftime('%H:%M:%S')} Uhr"


register_tool(
    "time",
    get_time,
    "Gibt die aktuelle Uhrzeit an"
)