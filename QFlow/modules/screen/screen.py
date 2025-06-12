"""
This module defines a decorator used to add a `name` attribute to screen classes.

The `screen` decorator is used to assign a unique name to a screen class. This name can 
be accessed through the `name` attribute of the decorated screen class. It also adds a 
`screenName` class-level attribute to the decorated class. Additionally, when `autoreloadUI`
is enabled, it ensures that the UI is properly reloaded upon screen display.
   
Note: The UI reload uses QTimer.singleShot with a delay of 0ms, which may introduce
a slight delay in UI updates as it processes the event in the next event loop cycle.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer

def screen(name: str, autoreloadUI: bool = False):
    """
    A decorator that adds a `name` attribute and showEvent method to a screen class.

    This decorator assigns a unique `name` to a screen class. The `name` is set as 
    both an instance attribute (`self.name`) and a class-level attribute (`screenName`).
    It also ensures that `showEvent` is added to execute the reloadUI method when the 
    screen is displayed. If `autoreloadUI` is enabled, it ensures that the UI method
    is properly called upon screen display.

    Args:
        name (str): The name to assign to the screen class.
        autoreloadUI (bool): If True, ensures the class has a `UI` method and reloads it on show.

    Returns:
        decorator: A class decorator that adds the following to the decorated class:
            - `name` attribute: The screen name as an instance attribute
            - `screenName` attribute: The screen name as a class attribute
            - `reloadUI()` method: Reloads the user interface
            - `setScreenName(name)` method: Changes the screen name
            - `showEvent` method: If autoreloadUI is True, reloads UI on show
    """

    def decorator(cls):
        """
        Decorates a class to add a `name` attribute and optionally reload the UI.

        Args:
            cls: The class to decorate.

        Returns:
            cls: The decorated class with a `name` attribute and UI reload support.
        """
        originalInit = cls.__init__

        if autoreloadUI:
            # Check if the class has a UI method
            if not hasattr(cls, 'UI') or not callable(getattr(cls, 'UI')):
                raise TypeError(f'The class {cls.__name__} must have a UI() method')

        def newInit(self, *args, **kwargs):
            """
            Initializes the decorated class and assigns the `name` attribute.

            Args:
                *args: Positional arguments passed to the original class initializer.
                **kwargs: Keyword arguments passed to the original class initializer.
            """
            self.name = name
            originalInit(self, *args, **kwargs)

            # Check if the class has a widgetParent
            if autoreloadUI and not hasattr(self, 'widgetParent'):
                raise TypeError(f'The class {cls.__name__} must have a widgetParent attribute')
        
        def removeAllLayouts(widget: QWidget):
            """
            Recursively removes all layouts and widgets from a given QWidget.

            Args:
                widget (QWidget): The widget from which all layouts and child widgets will be removed.
            """
            layout = widget.layout()
            
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().setParent(None)
                    if item.layout():
                        removeAllLayouts(item.layout())

            layout.deleteLater()
        
        def reloadUI(self):
            """
            Reloads the user interface by removing all existing layouts and
            re-executing the UI method after a short delay.
            
            Note: The delay is implemented using QTimer.singleShot(0, ...) which
            may introduce a slight delay in UI updates as it processes the event
            in the next event loop cycle.
            """
            if not hasattr(self, 'widgetParent'):
                raise TypeError(f'The class {cls.__name__} must have a widgetParent attribute')
            if not hasattr(cls, 'UI') or not callable(getattr(cls, 'UI')):
                raise TypeError(f'The class {cls.__name__} must have a UI() method')
            
            removeAllLayouts(self)
            QTimer.singleShot(0, lambda: self.UI(self.widgetParent))
        
        def setScreenName(self, name: str) -> None:
            """
            Changes the name of the screen.
            
            Args:
                name (str): The new name for the screen.
                
            Raises:
                ValueError: If name is empty or not a string.
            """
            if not name:
                raise ValueError("Screen name must be a non-empty string")
            
            self.name = name
            cls.screenName = name

        cls.__init__ = newInit
        cls.screenName = name
        cls.reloadUI = reloadUI
        cls.setScreenName = setScreenName

        if autoreloadUI:
            originalShowEvent = getattr(cls, 'showEvent', QWidget.showEvent)

            def showEvent(self, event):
                # Reload the UI after a short delay. Note: This line cost me 5 hours of debugging.
                QTimer.singleShot(0, lambda: reloadUI(self))
                originalShowEvent(self, event)

            cls.showEvent = showEvent

        return cls
    
    return decorator