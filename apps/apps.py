import os
import json
import time
from tools.tool_registry import register_tool

programs={}

CACHE_FILE=os.path.join(
    os.path.dirname(__file__),
    "program_cache.json"
)

CACHE_DURATION=60*60*24

def load_programs(force_refresh=False):

    global programs

    if not force_refresh and os.path.exists(CACHE_FILE):

        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as file:
                cache=json.load(file)

            timestamp=cache.get("timestamp", 0)

            if time.time() - timestamp < CACHE_DURATION:

                programs=cache.get("programs", {})

                print(f"{len(programs)} Programme aus Cache geladen")
                return

        except (json.JSONDecodeError, OSError):
            pass

    print("Suche installiert Programme...")

    programs.clear()

    search_paths=[
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expandvars(r"%LOCALAPPDATA%"),
    ]

    ignored_names={
        "uninstall.exe",
        "uninstaller.exe",
        "unins000.exe",
        "unins001.exe",
        "setup.exe",
        "installer.exe",
        "update.exe",
        "updater.exe",
    }

    for base_path in search_paths:

        if not os.path.exists(base_path):
            continue

        for root, dirs, files in os.walk(base_path):

            dirs[:]=[
                directory
                for directory in dirs
                if directory.lower() not in {
                    "cache",
                    "caches",
                    "temp",
                    "tmp"
                }
            ]

            for file in files:

                if not file.lower().endswith(".exe"):
                    continue

                if file.lower() in ignored_names:
                    continue

                name=os.path.splitext(file)[0].lower()
                full_path=os.path.join(root, file)

                if name not in programs:
                    programs[name]=full_path

    try:

        with open(CACHE_FILE, "w", encoding="utf-8") as file:

            json.dump(
                {
                    "timestamp":time.time(),
                    "programs":programs
                },
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError as e:
        print("CACHE FEHLER:", e)

    print(f"{len(programs)} Programme geladen")

def open_app(app_name):

    app_name = app_name.lower().strip()

    print("GESUCHT:", app_name)

    # 1. Exakten Treffer bevorzugen
    if app_name in programs:

        try:
            os.startfile(programs[app_name])

            print("EXAKTER TREFFER:", app_name)

            return f"Ich öffne {app_name}"

        except Exception as e:

            print("STARTFEHLER:", e)

            return "Fehler beim Öffnen"

    # 2. Teiltreffer suchen
    for program in programs:

        if app_name in program:

            print("TEILTREFFER:", program)
            print("PFAD:", programs[program])

            try:
                os.startfile(programs[program])

                print("START ERFOLGREICH")

                return f"Ich öffne {program}"

            except Exception as e:

                print("STARTFEHLER:", e)

                return "Fehler beim Öffnen"

    print("KEIN TREFFER")

    return "Programm nicht gefunden"

def start_app(app_name):
    """Öffnet eine instalierte Anwendung auf dem PC.
    
    Args:
        app_name: Name der Anwendung, z.B. "spotify", "chrome", "discord". Groß-/Kleinschreibung ist egal, auch Teilname wie "disc" für "discord" werden versucht.
        """
    return open_app(app_name)

register_tool(
    "open_app",
    "Öffnet eine installierte Anwendung.",
    start_app
)