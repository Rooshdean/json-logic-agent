__all__ = ["JsonLogicAgent"]


def __getattr__(name):
    if name == "JsonLogicAgent":
        from .agent import JsonLogicAgent
        return JsonLogicAgent
    raise AttributeError(name)
