import os
from tools.tool_registry import register_tool

programs={}

def load_programs():

    search_paths=[
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expandvars(r"%LOCALAPPDATA%"),
    ]

    for base_path in search_paths:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith(".exe"):
                    name=file.replace(".exe","").lower()
                    full_path=os.path.join(root,file)

                    if "uninstall" in name:
                        continue
                
                    if name not in programs:
                        programs[name]=full_path

                    print(f"{len(programs)} Programme geladen")

def open_app(app_name):
    
    app_name=app_name.lower()

    for program in programs:
        
        if app_name in program:

            try:
               os.startfile(programs[program])
               print("Gestartet")
               return f"Ich öffne {program}"
                
            except Exception as e:
               print("STARTFEHLER:", e)
               return "Fehler beim öffnen"
            
    return "Programm nicht gefunden"

def start_app(app):

    return open_app(app)

register_tool(
    "open_app",
    "Öffnet eine installierte Anwendung.",
    start_app,
    {
        "app_name": {
            "type": "string",
            "description": "Name der Anwendung",
            "required":True
        }
    }
)