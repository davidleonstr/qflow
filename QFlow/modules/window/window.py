from __future__ import annotations
"""
This module defines a Window class that provides window properties and screen management capabilities.
"""

from qtpy.QtWidgets import QStackedWidget, QWidget, QMainWindow
from qtpy.QtCore import QTimer, Qt
from typing import Dict
from QFlow.core.temp import INSTANCEARGS
from .params import WindowParams

class Window(QMainWindow):
    """
    A window class that provides window properties and screen management capabilities.

    This class allows you to configure the title, geometry, and icon of a window,
    while also providing built-in screen management functionality.
    """
    
    def __init__(
        self,
        **kwargs
    ):
        """
        Initializes the Window with specified properties and screen management.

        Args:
            name (str): The name of the window.
            title (str): The title of the window.
            geometry (list): The geometry of the window (ax: int, ay: int, aw: int, ah: int).
            maximizable (bool, optional): Determines whether the window can be maximized. Defaults to True.
            icon (QIcon): Callable of the icon to set for the window.
            customTemplate (QWidget): Callable of custom QWidget as a template. It needs to have a QStackedWidgets named 'screens' in order to render the screens there.
            parent: Parent widget.
            parentType: Expected parent type for validation.
            resizable (bool, optional): The ability to resize the window. Defaults to True.
            strictClosingWindows (bool, optional): Determines whether all windows should be closed when the window is closed. Defaults to True.
            opacity (float, optional): The opacity of the window.
            frameless (bool, optional): It can delete the window frame.
        """
        self.kwargs = WindowParams(**kwargs)

        super().__init__(self.kwargs.parent)
        
        # Initialize window properties
        self.name = self.kwargs.name
        self.title = self.kwargs.title
        self.windowGeometry = self.kwargs.geometry
        self.icon = self.kwargs.icon
        self.frameless = self.kwargs.frameless
        self.customTemplate = self.kwargs.customTemplate

        self.args = {}
        """
        Dictionary with the arguments passed from the window decorator.
        """
        
        # Initialize screen management
        self.screenHistory = []
        self.screens = {}
        self.windows = {}
        self.strictClosingWindows = self.kwargs.strictClosingWindows
        
        # Configure window
        self.setWindowTitle(self.title)
        self.setGeometry(*self.windowGeometry)

        if not self.kwargs.resizable:
            # The last two indices of the geometry are width and height
            width, height = self.kwargs.geometry[-2:]
            self.setFixedSize(width, height)
            self.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)

        if not self.kwargs.maximizable:
            currentFlags = self.windowFlags()
            # Remove maximize button while keeping other flags
            newFlags = currentFlags & ~Qt.WindowType.WindowMaximizeButtonHint
            self.setWindowFlags(newFlags | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)

        # Do that frameless
        if self.frameless:
            self.setWindowFlags(Qt.FramelessWindowHint)

        if self.kwargs.icon is not None:
            self.setWindowIcon(self.kwargs.icon())

        # Find and set the QStackedWidget in the custom template
        if self.customTemplate is not None:
            # Initialize template
            self.customTemplate: QWidget = self.kwargs.customTemplate(self)

            self.stackedScreens = self.customTemplate.findChild(QWidget, 'screens')

            # Raise
            if self.stackedScreens is None:
                raise Exception("Undefined 'screens' in your template.")

            self.setCentralWidget(self.customTemplate)
        else:
            self.stackedScreens = QStackedWidget()
            # Set normal
            self.setCentralWidget(self.stackedScreens)

        if self.kwargs.opacity != 1.0:
            self.setWindowOpacity(self.kwargs.opacity)

        self.opacity = self.kwargs.opacity

        # Validate parent type if specified
        if self.kwargs.parentType is not None and self.kwargs.parent is not None:
            if type(self.kwargs.parent) != self.kwargs.parentType:
                raise TypeError(
                    f"Window '{self.kwargs.name}' only accepts the parentType '{self.kwargs.parentType}' not '{type(self.kwargs.parent)}'."
                )

    def addScreen(self, screen: QWidget) -> None:
        """
        Adds a screen widget to the window's stacked widget.

        This method checks that the screen has a valid 'screenName' attribute and adds it 
        to the stacked widget for navigation.

        Args:
            screen (QWidget): The screen widget to add to the stacked widget.

        Raises:
            Exception: If the screen does not have a 'screenName' attribute.
        """
        if not hasattr(screen, 'screenName'):
            raise Exception(f"'{screen}' does not have screenName attribute.")
        
        name = screen.screenName
        self.screens[name] = screen
        self.stackedScreens.addWidget(screen)

    def setScreen(self, name: str, args: dict = None) -> None:
        """
        Sets the current screen to display based on the screen name.

        This method accepts a string name that must match the 'screenName' attribute
        of a previously added screen.

        Args:
            name (str): The name of the screen to display.
            args (dict): Arguments for the screen.

        Raises:
            Exception: If the specified screen does not exist.
        """
        if name in self.screens:
            currentScreen = self.stackedScreens.currentWidget()
            if currentScreen:
                self.screenHistory.append(currentScreen)

            screen = self.screens[name]
            if not hasattr(screen, 'screenName'):
                raise Exception(f"The screen '{screen}' does not have screenName attribute.")
            
            if args:
                INSTANCEARGS.setArgs(instance=screen, args=args)
            
            self.stackedScreens.setCurrentWidget(screen)      
        else:
            raise Exception(f"The screen '{name}' does not exist.")
            
    def goBack(self) -> None:
        """
        Navigates back to the previous screen in the screen history.
        """
        if self.screenHistory:
            previousScreen = self.screenHistory.pop()
            self.stackedScreens.setCurrentWidget(previousScreen)
    
    def setWindowName(self, name: str) -> None:
        """
        Changes the name of the window.
        
        Args:
            name (str): The new name for the window.
            
        Raises:
            ValueError: If name is empty or not a string.
        """
        if not name:
            raise ValueError("Window name must be a non-empty string.")
        
        self.name = name

    def showEvent(self, event):
        """   
        Args:
            event: The show event.
        """

        if hasattr(self, 'effect'):
            self.effect()

            # QMainWindow always has showEvent
            super().showEvent(event)

    def existScreen(self, name: str) -> bool:
        """
        Checks if a screen exists in the window.

        Args:
            name (str): The name of the screen.
        Returns:
            bool: True if the screen exists, False if it does not exist.
        """
        return name in self.screens

    def reloadScreens(self) -> None:
        """
        Reloads all window screens.
        """
        for name, screen in self.screens.items():
            if self.existScreen(name):
                screen.reloadUI()
    
    def reloadScreen(self, name: str) -> None:
        """
        Reloads a screen of the window.

        Args:
            name (str): The name of the screen to reload.
        """
        if self.existScreen(name):
            screen = self.screens[name]
            screen.reloadUI()

    def createWindow(self, window: "Window", args: dict = None) -> None:
        """
        Creates a new window and adds it to the windows dictionary for management.

        The window is created using the attributes 'windowGeometry', 'title', and 'name' 
        of the specified Window instance.

        Args:
            window (Window): The window to create.
            args (dict): Arguments for the window.

        Raises:
            Exception: If the window is missing any of the required attributes.
        """
        geometry = getattr(window, 'windowGeometry', None)
        title = getattr(window, 'title', None)
        name = getattr(window, 'name', None)

        if not geometry:
            raise Exception(f"The window '{window}' does not have a valid <windowGeometry>.")
        if not title:
            raise Exception(f"The window '{window}' does not have a valid <title>.")
        if not name:
            raise Exception(f"The window '{window}' does not have a valid <name>.")

        if not hasattr(self, 'windows'):
            self.windows = {}
        
        if not self.windows.get(name):
            window.closeEvent = lambda event: self.onWindowClose(event, name)
            self.windows[name] = window
            window.setGeometry(*geometry)
            window.setWindowTitle(title)

            if args:
                INSTANCEARGS.setArgs(instance=window, args=args)

            window.show()
        else:                
            print(f"The window '{name}' already exists.")

    def onWindowClose(self, event, name: str) -> None:
        """
        Handles the window close event and removes the window from the windows list.

        Args:
            event: The close event.
            name (str): The name of the window being closed.
        """
        if self.strictClosingWindows:
            # Close all child windows when any window is closed
            localWindow: Window = self.windows.get(name, None)

            if localWindow is not None:
                for windowName, windowInstance in list(localWindow.windows.items()):
                    windowInstance: Window
                    if windowName != name:  # Don't close the window that's already closing
                        windowInstance.close()
            else:
                for windowName, windowInstance in list(self.windows.items()):
                    windowInstance: Window
                    if windowName != name:  # Don't close the window that's already closing
                        windowInstance.close()      

        QTimer.singleShot(0, lambda: self.removeWindow(name))
        event.accept()

    def removeWindow(self, name: str) -> None:
        """
        Removes a window from the windows list.

        Args:
            name (str): The name of the window to remove.
        """
        if name in self.windows:
            del self.windows[name]

    def setWindow(self, name: str, args: dict = None) -> None:
        """
        Brings a specified window to the front and activates it.

        Args:
            name (str): The name of the window to bring to the front.
            args (dict): Arguments for the window.

        Raises:
            Exception: If the specified window does not exist.
        """
        if name in self.windows:
            self.windows[name].raise_()
            self.windows[name].activateWindow()

            if args:
                INSTANCEARGS.setArgs(instance=self.windows[name], args=args)

        else:
            raise Exception(f"The window '{name}' does not exist.")
            
    def closeWindow(self, name: str) -> None:
        """
        Closes a specified window.

        Args:
            name (str): The name of the window to close.

        Raises:
            Exception: If the specified window does not exist.
        """
        if name in self.windows:
            self.windows[name].close()
            del self.windows[name]
        else:
            raise Exception(f"The window '{name}' does not exist.")
    
    def removeScreen(self, name: str) -> None:
        """
        Removes a screen from the screens list.

        Args:
            name (str): The name of the screen to remove.
            
        Raises:
            Exception: If the screen does not exist.
        """
        if name not in self.screens:
            raise Exception(f"The screen '{name}' does not exist.")
        
        if hasattr(self, 'stackedScreens'):
            self.stackedScreens.removeWidget(self.screens[name])
        
        self.screens.pop(name)

    def existWindow(self, name: str) -> bool:
        """
        Checks if a window exists in the main window.

        Args:
            name (str): The name of the window.
        Returns:
            bool: True if the window exists, False if it does not exist.
        """
        return name in self.windows

    def reloadWindowScreens(self, window: str) -> None:
        """
        Reloads the screens of a window.

        Args:
            window (str): The name of the window to reload.
        """
        targetWindow: Window = self.windows.get(window)
        if targetWindow:
            targetWindow.reloadScreens()
    
    def reloadWindowScreen(self, window: str, screen: str) -> None:
        """
        Reloads a screen of a window.

        Args:
            window (str): The name of the window to reload.
            screen (str): The name of the screen to reload.
        """
        targetWindow: Window = self.windows.get(window)
        if targetWindow:
            targetWindow.reloadScreen(screen)
        
    def getScreenHistory(self) -> list:
        """
        Returns the current screen navigation history.
        
        Returns:
            list: List of screens in navigation history.
        """
        return self.screenHistory.copy()

    def clearScreenHistory(self) -> None:
        """
        Clears the screen navigation history.
        """
        self.screenHistory.clear()

    def getCurrentScreen(self) -> QWidget:
        """
        Gets the currently active screen.
        
        Returns:
            QWidget: The currently active screen widget.
        """
        return self.stackedScreens.currentWidget()

    def getAllScreens(self) -> Dict[str, QWidget]:
        """
        Gets all registered screens.
        
        Returns:
            Dict[str, QWidget]: Dictionary of all registered screens.
        """
        return self.screens.copy()

    def getAllWindows(self) -> Dict[str, "Window"]:
        """
        Gets all managed windows.
        
        Returns:
            Dict[str, Window]: Dictionary of all managed windows.
        """
        return self.windows.copy()
