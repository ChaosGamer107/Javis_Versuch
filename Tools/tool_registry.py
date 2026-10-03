import inspect

TOOLS={}

def register_tool(name, description, function):
    TOOLS[name]={
        "description":description,
        "function":function,
    }

def get_tool(name):

    return TOOLS.get(name)

def _parse_param_docs(function):

    doc=inspect.getdoc(function)

    if not doc:
        return {}

    param_docs={}
    in_args=False

    for line in doc.splitlines():

        stripped=line.strip()

        if stripped.lower() in ("args:", "arguments:", "parameters:"):
            in_args=True
            continue

        if not in_args:
            continue

        if not stripped:
            break

        if ":" not in stripped:
            continue

        name_part, _, description=stripped.partition(":")
        name_part=name_part.split("(")[0].strip()

        param_docs[name_part]=description.strip()

    return param_docs

def get_tools():

    tools=[]

    for name, tool in TOOLS.items():

        function=tool["function"]

        signature=inspect.signature(function)
        param_docs=_parse_param_docs(function)

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
                "description":param_docs.get(
                    parameter.name,
                    f"Parameter {parameter.name}"
                )
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
        