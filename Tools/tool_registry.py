TOOLS={}

def register_tool(name, description, function, parameters:None, examples):
    TOOLS[name]={
        "description":description,
        "function":function,
        "parameters":parameters or {},
        "triggers":triggers or {}
    }

def get_tool(name):

    return TOOLS.get(name)

def get_tool_description():

    text=""

    for name, tool in TOOLS.items():

        text+=f"\n{name}: "
        text+=f"\nBeschreibung: {tool['description']}"

        if tool["parameters"]:

            text+=f"\n Parameter:"

            for parameter, info in tool["parameters"].items():

                text+=(
                    f"\n    -{parameter}:"
                    f"{info.get('description', '')}"
                )    

        else:

            text+=f"\n Parameter: keine"

        text+=f"\n"

    return text
        