import inspect

TOOLS={}

def register_tool(name, description, function):
    TOOLS[name]={
        "description":description,
        "function":function,
    }

def get_tool(name):

    return TOOLS.get(name)

def get_tools():

    tools=[]

    for name, tool in TOOLS.items():

        function=tool["function"]

        signature=inspect.signature(function)

        properties={}
        required=[]

        for parameter in signature.parameters.values():

            if parameter.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD
            ):
                continue

            parameter_type="string"

            if parameter.annotation is int:
                parameter_type="integer"

            elif parameter.annotation is float:
                parameter_type="number"

            elif parameter.annotation is bool:
                parameter_type="boolean"

            properties[parameter.name]={
                "type":parameter_type,
                "description":f"Parameter {parameter.name}"
            }

            if parameter.default is inspect.Parameter.empty:
                required.append(parameter.name)

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
        