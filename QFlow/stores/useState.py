"""
useState module provides a state management system for Python applications.
"""

from typing import Any, Callable, List, Tuple

class State:
    """
    A class that implements state management with subscription capabilities.
    
    This class provides a simple way to manage state in an application, with the ability
    to subscribe to state changes. It's designed to be used with the useState function
    to provide a React-like state management experience.
    
    Attributes:
        _value (Any): The current state value.
        _callbacks (List[Callable]): List of callback functions to be called when the state changes.
    """
    
    def __init__(self, initialValue: Any) -> None:
        """
        Initialize a new State instance.
        
        Args:
            initialValue (Any): The initial state value.
        """
        self._value = initialValue
        self._callbacks: List[Callable[[Any], None]] = []

    def get(self) -> Any:
        """
        Get the current state value.
        
        Returns:
            Any: The current state value.
        """
        return self._value

    def set(self, newValue: Any) -> None:
        """
        Set a new state value and notify all subscribers if the value has changed.
        
        Args:
            newValue (Any): The new state value to set.
        """
        if newValue != self._value:
            self._value = newValue
            self._notify_subscribers()

    def subscribe(self, callback: Callable[[Any], None]) -> None:
        """
        Subscribe a callback function to be called when the state changes.
        
        Args:
            callback (Callable[[Any], None]): The function to be called when the state changes.
                                             The function should accept one parameter of any type.
        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def unsubscribe(self, callback: Callable[[Any], None]) -> None:
        """
        Unsubscribe a previously registered callback function.
        
        Args:
            callback (Callable[[Any], None]): The callback function to remove from subscribers.
        """
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def _notify_subscribers(self) -> None:
        """
        Notify all subscribers of the state change.
        This method is called internally when the state changes.
        """
        for callback in self._callbacks:
            try:
                callback(self._value)
            except Exception as e:
                print(f"Error in state subscriber callback: {e}")

def useState(initialValue: Any) -> Tuple[Callable[[], Any], Callable[[Any], None], Callable[[Callable[[Any], None]], None]]:
    """
    Create a new state with getter, setter, and subscriber functions.
    
    This function provides a React-like useState hook experience, returning a tuple of
    functions to get the current state value, set a new state value, and subscribe to
    state changes.
    
    Args:
        initialValue (Any): The initial state value.
        
    Returns:
        Tuple[Callable[[], Any], Callable[[Any], None], Callable[[Callable[[Any], None]], None]]:
            A tuple containing:
            - A function to get the current state value
            - A function to set a new state value
            - A function to subscribe to state changes
    """
    state = State(initialValue)
    return state.get, state.set, state.subscribe