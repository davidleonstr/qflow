"""
useState module provides a state management system for Python applications.
"""

from typing import Any, Callable, List

class State:
    """
    A class that implements state management with subscription capabilities.
    
    This class provides a simple way to manage state in an application, with the ability
    to subscribe to state changes. It's designed to be used with the useState function
    to provide a React-like state management experience.
    
    Attributes:
        _value (Any): The current state value.
        callbacks (List[Callable]): List of callback functions to be called when the state changes.
    """
    
    def __init__(self, initialValue: Any) -> None:
        """
        Initialize a new State instance.
        
        Args:
            initialValue (Any): The initial state value.
        """
        self.value = initialValue
        self.callbacks: List[Callable[[Any], None]] = []

    def get(self) -> Any:
        """
        Get the current state value.
        
        Returns:
            Any: The current state value.
        """
        return self.value

    def set(self, newValue: Any) -> None:
        """
        Set a new state value and notify all subscribers if the value has changed.
        
        Args:
            newValue (Any): The new state value to set.
        """
        if newValue != self.value:
            self.value = newValue
            self.notifySubscribers()

    def subscribe(self, callback: Callable[[Any], None]) -> None:
        """
        Subscribe a callback function to be called when the state changes.
        
        Args:
            callback (Callable[[Any], None]): The function to be called when the state changes.
                                             The function should accept one parameter of any type.
        """
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def unsubscribe(self, callback: Callable[[Any], None]) -> None:
        """
        Unsubscribe a previously registered callback function.
        
        Args:
            callback (Callable[[Any], None]): The callback function to remove from subscribers.
        """
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def notifySubscribers(self) -> None:
        """
        Notify all subscribers of the state change.
        This method is called internally when the state changes.
        """
        for callback in self.callbacks:
            try:
                callback(self.value)
            except Exception as e:
                print(f"Error in state subscriber callback: '{e}'.")