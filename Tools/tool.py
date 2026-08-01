from tool_registry import get_tool

def execute_tool(name, arguments):

    tool=get_tool(name)

    if tool is None:
        return "Dieses Tool existiert nicht."

    try:

        return tool["function"](**arguments)

    except Exception as e:

        return f"Fehler: {e}"