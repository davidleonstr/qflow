from typing import Any

class InstanceArgs:
    def __init__(self):
        self.args: dict = {}
    
    def setArg(self, instance: Any, name: str, value: Any) -> None:
        self.args[id(instance)][name] = value
    
    def getArg(self, instance: Any, name: str) -> Any:
        if not id(instance) in self.args:
            return None
        
        if not name in self.args[id(instance)]:
            return None
            
        return self.args[id(instance)][name]
    
    def existArg(self, instance: Any, name: str) -> bool:
        return name in self.args[id(instance)]

    def getArgs(self, instance: Any,) -> dict:
        if not id(instance) in self.args:
            return {}
        
        return self.args[id(instance)]

    def setArgs(self, instance: Any, args: dict) -> None:
        self.args[id(instance)] = {}
        
        for key, value in args.items():
            self.args[id(instance)][key] = value
    
INSTANCEARGS = InstanceArgs()