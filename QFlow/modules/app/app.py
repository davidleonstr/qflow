"""
This module defines an App class that inherits from Window and provides
application-level functionality with support for multiple screens and window management.
"""
from qtpy.QtCore import Qt
from QFlow.modules.window import Window
from qtpy.QtWidgets import QApplication
import sys
from QFlow.modules.window import WindowParams
from dataclasses import asdict

class App(Window):
    """
    An application class that extends Window functionality for main application windows.
    
    This class provides all the functionality of a Window plus additional application-level
    features like strict window management and enhanced screen handling.
    """
    
    def __init__(
        self,
        **kwargs
    ):
        """
        Initializes the App with application-specific settings.

        Args:
            title (str): The title to set for the application window.
            geometry (list): The window geometry as a list [x, y, width, height].
            icon (QIcon): Callable of the icon to set for the window.
            name (str, optional): The name of the application window. Defaults to "App".
            customTemplate (QWidget): Callable of custom QWidget as a template. It needs to have a QStackedWidgets named 'screens' in order to render the screens there.
            resizable (bool, optional): Determines whether the window can be resized. Defaults to True.
            maximizable (bool, optional): Determines whether the window can be maximized. Defaults to True.
            strictClosingWindows (bool, optional): Determines whether all windows should be closed when the main window is closed. Defaults to True.
            opacity (float, optional): The opacity of the window. Defaults to 1.0.
            frameless (bool, optional): It can delete the window frame.
        """
        # Initialize the parent Window class

        self.windowParams = WindowParams(**kwargs)

        super().__init__(
            **asdict(self.windowParams)
        )
        
        # Application-specific properties
        self.maximizable = self.windowParams.maximizable
        
        # Configure window properties
        self.configureWindowProperties(
            self.windowParams.resizable, 
            self.windowParams.maximizable, 
            self.windowParams.geometry
        )
        
        # Set up close event handler
        self.closeEvent = lambda event: self.onWindowClose(event, self.name)

    def configureWindowProperties(self, resizable: bool, maximizable: bool, geometry: list[int]) -> None:
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
    
    def run(self, QApp: QApplication):
        self.show()
        sys.exit(QApp.exec())