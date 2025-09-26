"""
This module defines an App class that inherits from Window and provides
application-level functionality with support for multiple screens and window management.
"""
from qtpy.QtCore import QTimer, Qt
from qtpy.QtGui import QIcon
from typing import Callable, Dict
from ..window import Window
from qtpy.QtWidgets import QApplication
import sys

class App(Window):
    """
    An application class that extends Window functionality for main application windows.
    
    This class provides all the functionality of a Window plus additional application-level
    features like strict window management and enhanced screen handling.
    """
    
    def __init__(
        self,
        title: str,
        geometry: list[int],
        icon: Callable[[], QIcon],
        name: str = 'App',
        resizable: bool = True,
        maximizable: bool = True,
        strictClosingWindows: bool = True,
        opacity: float = 1.0,
        animatedEvents: Dict[str, bool] = None,
        animationValues: Dict[str, float] = None
    ):
        """
        Initializes the App with application-specific settings.

        Args:
            title (str): The title to set for the application window.
            geometry (list): The window geometry as a list [x, y, width, height].
            icon (Callable[[], QIcon]): Callable to make the icon to set for the window.
            name (str, optional): The name of the application window. Defaults to "App".
            resizable (bool, optional): Determines whether the window can be resized. Defaults to True.
            maximizable (bool, optional): Determines whether the window can be maximized. Defaults to True.
            strictClosingWindows (bool, optional): Determines whether all windows should be closed when the main window is closed. Defaults to True.
            opacity (float, optional): The opacity of the window. Defaults to 1.0.
            animatedEvents (Dict[str, bool], optional): Default animations for events.
            animationValues (Dict[str, float], optional): Default values for animations.
        """
        # Initialize the parent Window class
        super().__init__(
            name=name,
            title=title,
            geometry=geometry,
            icon=icon,
            parent=None,
            parentType=None,
            resizable=resizable,
            strictClosingWindows=strictClosingWindows,
            opacity=opacity,
            animatedEvents=animatedEvents,
            animationValues=animationValues,
            maximizable=maximizable
        )
        
        # Application-specific properties
        self.maximizable = maximizable
        
        # Configure window properties
        self._configureWindowProperties(resizable, maximizable, geometry)
        
        # Set up close event handler
        self.closeEvent = self._onAppClose

    def _configureWindowProperties(self, resizable: bool, maximizable: bool, geometry: list[int]) -> None:
        """
        Configures window properties based on the provided settings.
        
        Args:
            resizable (bool): Whether the window should be resizable.
            maximizable (bool): Whether the window should be maximizable.
            geometry (list[int]): The window geometry.
        """
        if not resizable:
            # The last two indices of the geometry are width and height
            width, height = geometry[-2:]
            self.setFixedSize(width, height)
            self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)
        
        if not maximizable:
            currentFlags = self.windowFlags()
            # Remove maximize button while keeping other flags
            newFlags = currentFlags & ~Qt.WindowType.WindowMaximizeButtonHint
            self.setWindowFlags(newFlags | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)

    def _onWindowClose(self, event, name: str) -> None:
        """
        Handles window close events with application-specific logic.

        Args:
            event: The close event.
            name (str): The name of the window being closed.
        """
        if self.strictClosingWindows:
            # Close all child windows when any window is closed
            for windowName, window_instance in list(self.windows.items()):
                if windowName != name:  # Don't close the window that's already closing
                    window_instance.close()

        # Remove the window from management after a short delay
        QTimer.singleShot(0, lambda: self.removeWindow(name))
        event.accept()

    def _onAppClose(self, event) -> None:
        """
        Handles the main application close event.

        Args:
            event: The close event.
        """
        if self.strictClosingWindows:
            # Close all managed windows when the main application closes
            for _, window in self.windows.items():
                window.close()

        event.accept()
    
    def run(self, QApp: QApplication):
        self.show()
        sys.exit(QApp.exec())