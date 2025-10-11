from typing import Any

class InstanceArgs:
    """
    Manages dynamic arguments/attributes for object instances using their unique IDs.
    
    This class allows associating arbitrary arguments to any object instance,
    using the object's unique ID as a key. It's useful for adding metadata or
    temporary properties to objects without modifying their original class.
    
    Attributes:
        args (dict): Dictionary that maps instance IDs to their associated arguments.
                    Structure: {instance_id: {arg_name: arg_value, ...}, ...}
    """
    
    def __init__(self):
        """
        Initializes a new InstanceArgs instance.
        
        Creates an empty dictionary to store instance arguments.
        """
        self.args: dict = {}
    
    def setArg(self, instance: Any, name: str, value: Any) -> None:
        """
        Sets a specific argument for a given instance.
        
        If the instance doesn't exist in the registry, a new entry
        is automatically created for it.
        
        Args:
            instance (Any): The object instance to assign the argument to.
            name (str): Name of the argument/attribute.
            value (Any): Value to assign to the argument.
        """
        instance_id = id(instance)
        if instance_id not in self.args:
            self.args[instance_id] = {}
        self.args[instance_id][name] = value
    
    def getArg(self, instance: Any, name: str) -> Any:
        """
        Gets the value of a specific argument for an instance.
        
        Args:
            instance (Any): The object instance to get the argument from.
            name (str): Name of the argument to retrieve.
        
        Returns:
            Any: The value of the argument, or None if the instance or argument doesn't exist.
        """
        if not id(instance) in self.args:
            return None
        
        if not name in self.args[id(instance)]:
            return None
            
        return self.args[id(instance)][name]
    
    def existArg(self, instance: Any, name: str) -> bool:
        """
        Checks if a specific argument exists for an instance.
        
        Args:
            instance (Any): The object instance to check.
            name (str): Name of the argument to check for.
        
        Returns:
            bool: True if the argument exists, False otherwise.
        
        Note:
            This method will raise a KeyError if the instance doesn't exist
            in the registry. Consider checking with getArgs() first or
            handle the exception appropriately.
        """
        return name in self.args[id(instance)]

    def getArgs(self, instance: Any) -> dict:
        """
        Gets all arguments for a specific instance.
        
        Args:
            instance (Any): The object instance to get arguments from.
        
        Returns:
            dict: Dictionary containing all arguments for the instance,
                 or an empty dict if the instance doesn't exist.
        """
        if not id(instance) in self.args:
            return {}
        
        return self.args[id(instance)]

    def setArgs(self, instance: Any, args: dict) -> None:
        """
        Sets multiple arguments for an instance at once.
        
        This method replaces all existing arguments for the instance
        with the provided dictionary.
        
        Args:
            instance (Any): The object instance to set arguments for.
            args (dict): Dictionary containing argument names and values.
        """
        self.args[id(instance)] = {}
        
        for key, value in args.items():
            self.args[id(instance)][key] = value
    
    def clearArgs(self, instance: Any) -> None:
        """
        Clears all arguments.

        Args:
            instance (Any): The object instance to set arguments for.
        """
        self.args[id(instance)] = {}