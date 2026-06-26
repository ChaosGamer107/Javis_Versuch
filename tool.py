from commands import get_time, open_youtube
from apps import open_app

TOOLS={
    "time":get_time,
    "youtube":open_youtube,
}

def execute_tool(action, arguments=None):

    if arguments is None:
        arguments={}

    if action=="open_app":
        return open_app(arguments.get("app",""))
    
    if action in TOOLS:
        return TOOLS[action]()
    
    return "Dieses Tool kenn ich noch nicht"