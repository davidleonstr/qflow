"""
This module defines a decorator that assigns screen properties and screen management capabilities
to a class.
"""

from ...core import QWidget, QTimer

def screen(name: str, autoreloadUI: bool = False):
    """
    Args:
        name (str): The name to assign to the screen class.
        autoreloadUI (bool): If True, ensures the class has a `UI` method and reloads it on show.
    """

    def decorator(cls):
        """
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
            self.screenName = self.name

            originalInit(self, *args, **kwargs)

            # Check if the class has a screenParent
            if autoreloadUI and not hasattr(self, 'screenParent'):
                raise TypeError(f'The class {cls.__name__} must have a screenParent attribute')
        
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
            Reloads the interface.
            """
            if not hasattr(self, 'screenParent'):
                raise TypeError(f'The class {cls.__name__} must have a screenParent attribute')
            if not hasattr(cls, 'UI') or not callable(getattr(cls, 'UI')):
                raise TypeError(f'The class {cls.__name__} must have a UI() method')
            
            removeAllLayouts(self)
            QTimer.singleShot(0, lambda: self.UI(self.screenParent))
        
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

        cls.__init__ = newInit
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