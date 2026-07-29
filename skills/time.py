from datetime import datetime
from apps.tool_registry import register_tool

def get_time():
    
    now = datetime.now()
    
    return f"Es ist {now.strftime('%H:%M:%S')} Uhr"


register_tool(
    name="time",
    description="Gibt die aktuelle Uhrzeit zurück.",
    paramters=[],
    function=get_time
)