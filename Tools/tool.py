from Tools.tool_registry import get_tool

def execute_tool(name, arguments):

    tool=get_tool(name)

    if tool is None:
        return f"Das Tool '{name}' existiert nicht."

    if arguments is None:
        arguments={}

    try:

        result=tool["function"](**arguments)

        return result

    except Exception as error:

        return f"Fehler beim Ausführen von '{name}': {error}"