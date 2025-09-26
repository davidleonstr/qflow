from ..core.temp import INSTANCE_ARGS
from typing import Any

class Params:
    def __init__(self, instance: Any):
        self.identity = instance

    def get(self, name: str = None) -> dict | Any:
        if name is not None:
            return INSTANCE_ARGS.getArg(instance=self.identity, name=name)
        else:
            return INSTANCE_ARGS.getArgs(instance=self.identity)
    
    def set(self, name: str = None, value: Any = None, args: dict = None) -> None:
        if args:
            INSTANCE_ARGS.setArgs(instance=self.identity, args=args)
        else: 
            INSTANCE_ARGS.setArg(instance=self.identity, name=name, value=value)
    
    def exist(self, name: str) -> bool:
        return INSTANCE_ARGS.existArg(instance=self.identity, name=name)