TOOLS={}

def register_tool(name,description, parameters, function):
    TOOLS[name]={
        "description":description,
        "parameters":parameters,
        "function":function
    }

def execute_toll(action, arguments=None):

    if arguments is None:
        arguments={}

    tool=TOOLS.get(action)

    if tool is None:
        return f"Unbekanntes Tool: {action}"

    return TOOLS["function"](**arguments)

def get_tool_discription():

    text=""

    for name, tool in TOOLS.items():

        text+=f"""
    Tool:

    {name}

    Beschreibung:

    {tool["description"]}

    Parameter:

    {", ".join(tool["parameters"])if tool["parameters"] else "Keine"}

"""
        
        return text
        