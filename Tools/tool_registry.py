TOOLS={}

def register_tool(name, description, function, parameters:None):
    TOOLS[name]={
        "description":description,
        "function":function,
        "parameters":parameters or {},
    }

def get_tool(name):

    return TOOLS.get(name)

def get_tools():

    tools=[]

    for name, tool in TOOLS.items():

        properties={}

        required={}

        for parameter, info in tool["parameters"].items():

            properties[parameter]={
                "type":info.get("type", "string"),
                "description":info.get("description", "")
            }

            if info.get("required", True):
                required.append(parameter)

        tools.append({
            "type":"function",
            "function":{
                "name":name,
                "description":tool["description"],
                "parameters":{
                    "type":"object",
                    "properties":properties,
                    "required":required
                }
            }
        })

    return tools
        