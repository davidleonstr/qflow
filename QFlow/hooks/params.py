from ..core import INSTANCEARGS
from typing import Any

class Params:
    def __init__(self, instance: Any):
        self.identity = instance

    def get(self, name: str = None) -> dict | Any:
        if name is not None:
            return INSTANCEARGS.getArg(instance=self.identity, name=name)
        else:
            return INSTANCEARGS.getArgs(instance=self.identity)
    
    def set(self, name: str = None, value: Any = None, args: dict = None) -> None:
        if args:
            INSTANCEARGS.setArgs(instance=self.identity, args=args)
        else: 
            INSTANCEARGS.setArg(instance=self.identity, name=name, value=value)
    
    def exist(self, name: str) -> bool:
        return INSTANCEARGS.existArg(instance=self.identity, name=name)