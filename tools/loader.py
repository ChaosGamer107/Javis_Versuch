import importlib
import pkgutil
import tools

def load_tools():

    for module in pkgutil.iter_modules(tools.__path__):

        name=module.name

        if name.startswith("_"):
            continue

        if name in {
            "tool",
            "tool_registry",
            "loader"
        }:
            continue

        importlib.import_module(
            f"tools.{name}"
        )