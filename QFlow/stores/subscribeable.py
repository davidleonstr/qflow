"""
Subscribeable module provides a base class for implementing the Observer pattern in Python.
This module is part of the Qurderer framework and is used for state management and reactivity.
"""

from typing import Any, Callable, List, Optional

class Subscribeable:
    """
    A base class that implements the Observer pattern, allowing objects to subscribe to value changes.
    
    This class provides a simple way to implement reactive programming patterns, where subscribers
    are notified whenever the value changes. It's particularly useful for UI components that need
    to react to state changes.
    
    Attributes:
        _value (Any): The current value stored in the Subscribeable instance. Planned for package use only.
        _callbacks (List[Callable]): List of callback functions to be called when the value changes. Planned for package use only.
    """
    
    def __init__(self, initialValue: Optional[Any] = None) -> None:
        """
        Initialize a new Subscribeable instance.
        
        Args:
            initialValue (Optional[Any], optional): The initial value. Defaults to None.
        """
        self._value = initialValue
        self._callbacks: List[Callable[[Any], None]] = []

    def subscribe(self, callback: Callable[[Any], None]) -> None:
        """
        Subscribe a callback function to be called when the value changes.
        
        Args:
            callback (Callable[[Any], None]): The function to be called when the value changes.
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

    @property
    def value(self) -> Any:
        """
        Get the current value.
        
        Returns:
            Any: The current value stored in this instance.
        """
        return self._value

    @value.setter
    def value(self, newValue: Any) -> None:
        """
        Set a new value and notify all subscribers if the value has changed.
        
        Args:
            newValue (Any): The new value to set.
        """
        if newValue != self._value:
            self._value = newValue
            self._notify_subscribers()

    def _notify_subscribers(self) -> None:
        """
        Notify all subscribers of the value change.
        This method is called internally when the value changes.
        """
        for callback in self._callbacks:
            try:
                callback(self._value)
            except Exception as e:
                print(f"Error in subscriber callback: {e}")