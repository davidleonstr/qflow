"""
This module defines a Screen class that assigns screen properties and screen management capabilities
to a class through inheritance or composition.
"""

from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QWidget
from QFlow.modules.window import Window
from .params import ScreenParams

class Screen(QWidget):
    """
    A class that provides screen properties and screen management capabilities.
    Can be used as a base class or through composition.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the Screen object.
        
        Args:
            name (str): The name to assign to the screen.
            autoreloadUI (bool): If True, ensures the class has a `UI` method and reloads it on show.
            autoUI (bool): Executes the UI function during __init__ without having to call it.
            parentType: Expected parent type for validation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.kwargs = ScreenParams(**kwargs)

        super().__init__(self.kwargs.parent)
        
        self.name = self.kwargs.name

        self.args = {}
        """
        Dictionary with the arguments passed from the screen decorator.
        """
        
        self.screenName = self.name
        self.parentType = self.kwargs.parentType
        self.autoreloadUI = self.kwargs.autoreloadUI
        self.autoUI = self.kwargs.autoUI
        self.loaded = False
        
        if self.kwargs.autoreloadUI:
            # Check if the class has a UI method
            if not hasattr(self, 'UI') or not callable(getattr(self, 'UI')):
                raise TypeError(f"The class '{self.__class__.__name__}' must have a UI() method.")
        
        # Store original parent method if it exists
        if hasattr(super(), 'parent'):
            originalParent = super().parent
            # Get the real parent, not the QStackedWidget
            parent = originalParent()
            self.parent = lambda: parent
        
        # Validate parent type if specified
        if self.kwargs.parentType is not None and hasattr(self, 'parent'):
            parent = self.parent()
            if parent and hasattr(parent, '__class__') and hasattr(parent.__class__, '__bases__'):
                if parent.__class__.__bases__[0] != self.kwargs.parentType:
                    raise TypeError(
                        f"Screen '{self.kwargs.name}' only accepts the parentType '{self.kwargs.parentType}' not '{parent.__class__.__bases__[0]}'."
                    )
                       
    def parent(self) -> Window: ...
    
    @staticmethod
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
                    Screen.removeAllLayouts(item.layout())

            layout.deleteLater()
    
    def reloadUI(self):
        """
        Reloads the interface.
        """
        if not hasattr(self, 'UI') or not callable(getattr(self, 'UI')):
            raise TypeError(f"The class '{self.__class__.__name__}' must have a UI() method")
        
        Screen.removeAllLayouts(self)
        QTimer.singleShot(0, lambda: self.UI())
    
    def setScreenName(self, name: str) -> None:
        """
        Changes the name of the screen.
        
        Args:
            name (str): The new name for the screen.
            
        Raises:
            ValueError: If name is empty or not a string.
        """
        if not name:
            raise ValueError("Screen name must be a non-empty string.")
        
        self.name = name
        self.screenName = name
    
    def showEvent(self, event):
        """
        Override showEvent to handle UI reloading and effects.
        
        Args:
            event: The show event.
        """
        if self.autoreloadUI:
            # Reload the UI after a short delay. Note: This line cost me 5 hours of debugging.
            QTimer.singleShot(0, lambda: self.reloadUI())

        if not self.autoreloadUI and self.autoUI and not self.loaded:
            # Execute the UI if autoUI
            QTimer.singleShot(0, lambda: self.UI())
            # Specifies that the screen has already been loaded
            self.loaded = True

        if hasattr(self, 'effect'):
            self.effect()

        # Call parent's showEvent if it exists
        if hasattr(super(), 'showEvent'):
            super().showEvent(event)