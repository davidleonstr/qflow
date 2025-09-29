from ..core.temp import INSTANCE_ARGS
from typing import Any

class Params:
    """
    Manages parameters associated with a specific instance.
    
    This class provides an interface to get, set, and verify the existence
    of parameters stored for a given instance.
    
    Attributes:
        identity (Any): The instance for which parameters are managed.
    """
    
    def __init__(self, instance: Any):
        """
        Initializes the parameter manager for a specific instance.
        
        Args:
            instance (Any): The instance whose parameters will be managed.
        """
        self.identity = instance

    def get(self, name: str = None) -> dict | Any:
        """
        Gets one or all parameters from the instance.
        
        Args:
            name (str, optional): The name of the parameter to get. 
                If None, returns all parameters. Defaults to None.
        
        Returns:
            dict | Any: If name is None, returns a dictionary with all 
                parameters. If name is specified, returns the parameter value 
                or None if it doesn't exist.
        """
        if name is not None:
            return INSTANCE_ARGS.getArg(instance=self.identity, name=name)
        else:
            return INSTANCE_ARGS.getArgs(instance=self.identity)
    
    def set(self, name: str = None, value: Any = None, args: dict = None) -> None:
        """
        Sets one or multiple parameters for the instance.
        
        Args:
            name (str, optional): The name of the parameter to set. 
                Ignored if args is specified.
            value (Any, optional): The value of the parameter to set.
                Ignored if args is specified.
            args (dict, optional): Dictionary with multiple parameters to set.
                If provided, takes priority over name and value.
        
        Returns:
            None
        """
        if args:
            INSTANCE_ARGS.setArgs(instance=self.identity, args=args)
        else: 
            INSTANCE_ARGS.setArg(instance=self.identity, name=name, value=value)
    
    def exist(self, name: str) -> bool:
        """
        Checks if a parameter exists for the instance.
        
        Args:
            name (str): The name of the parameter to check.
        
        Returns:
            bool: True if the parameter exists, False otherwise.
        """
        return INSTANCE_ARGS.existArg(instance=self.identity, name=name)