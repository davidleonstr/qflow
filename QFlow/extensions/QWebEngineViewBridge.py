"""
This module defines the QWebEngineViewBridge class, which extends QObject to provide communication
between QWebEngineView (JavaScript) and Python.

The class allows registering Python functions that can be invoked from JavaScript
through Qt's WebChannel system.
"""

from qtpy.QtCore import QObject, Slot
from typing import Callable

class QWebEngineViewBridge(QObject):
    """
    Planned for package use only.

    A QObject subclass that acts as a bridge between JavaScript and Python.

    This class stores callable Python functions and allows them to be executed
    dynamically by name, typically from JavaScript using QWebChannel.
    """

    def __init__(self):
        """
        Initializes a QWebEngineViewBridge instance.

        Attributes:
            functions (dict): A dictionary mapping function names (str)
                              to callable Python functions.
        """
        super().__init__()

        self.functions = {}

    def add(self, name: str, callable: Callable):
        """
        Registers a function in the QWebEngineViewBridge.

        Args:
            name (str): The name used to identify the function.
            callable (Callable): The function to be executed.
        """
        self.functions[name] = callable
    
    def delete(self, name: str):
        """
        Removes a function from the QWebEngineViewBridge.

        Args:
            name (str): The name of the function to remove.
        """
        del self.functions[name]

    @Slot(str)
    def execute(self, name: str, *args):
        """
        Executes a registered function by name.

        Args:
            name (str): The name of the function to execute.
            *args: Arguments passed to the function.

        Note:
            This method is exposed to JavaScript via QWebChannel.
        """
        if name in self.functions:
            self.functions[name](*args)