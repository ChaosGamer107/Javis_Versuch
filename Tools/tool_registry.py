TOOLS={}

def register_tool(name,description, function):
    TOOLS[name]={
        "description":description,
        "function":function
    }

def get_tool(name):

    return TOOLS.get(name)

def get_tool_description():

    text=""

    for name, tool in TOOLS.items():

        text+=f"{name}: {tool['description']}\n"

    return text
        