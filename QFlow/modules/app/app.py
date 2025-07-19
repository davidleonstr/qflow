"""
This module defines a decorator that can be used to create a app with support for
multiple screens and window management.
"""

from ...core import QWidget, QStackedWidget, QMainWindow, QTimer, QIcon, xQt, QFlowDevConfiguration
from typing import Callable
from ..window import WindowTyping
from ..screen import ScreenTyping

def app(
        title: str, 
        geometry: list[int], 
        icon: Callable[[], QIcon], 
        resizable: bool = True, 
        maximizable: bool = True,
        strictClosingWindows: bool = True
    ):
    """
    A decorator that adds window management functionality to a class.

    Args:
        title (str): The title to set for the window.
        geometry (list): The window geometry as a list [x, y, width, height].
        icon (QIcon): Callable to make the icon to set for the window.
        resizable (bool, optional): Determines whether the window can be resized. Defaults to True.
        maximizable (bool, optional): Determines whether the window can be maximized. Defaults to True.
        strictClosingWindows (bool, optional): Determines whether all windows should be closed when the main window is closed. Defaults to True.
    
    Returns:
        decorator: A class decorator that adds window management functionality to the class.
    """

    def decorator(cls):
        """
        Decorates a class to add window management functionality.
        """

        originalInit = cls.__init__

        def newInit(self, *args, **kwargs):
            """
            Initializes the decorated class with window settings and stacked screens.

            Sets the window title, geometry, and icon, and initializes the stacked widget
            to manage multiple screens.

            Args:
                *args: Positional arguments passed to the original class initializer.
                **kwargs: Keyword arguments passed to the original class initializer.
            """
            # The main window's features are initialized. Before the original __init__
            self.screens = {}
            self.windows = {}
            self.windowGeometry = geometry
            self.screenHistory = []
            self.title = title
            self.icon = icon
            self.stackedScreens = QStackedWidget()

            self.closeEvent = lambda event: onAppClose(self, event)
            self.strictClosingWindows = strictClosingWindows

            originalInit(self, *args, **kwargs)

            self.setWindowTitle(title)
            self.setGeometry(*geometry)
            self.setWindowIcon(icon())

            if not resizable:
                # The last two indices of the geometry are obtained
                ah, aw = self.windowGeometry[-2:]
                self.setFixedSize(ah, aw)
                self.setWindowFlags(xQt.WindowType.WindowMinimizeButtonHint | xQt.WindowType.WindowCloseButtonHint)
            
            if not maximizable:
                self.setWindowFlags(xQt.WindowType.WindowMinimizeButtonHint | xQt.WindowType.WindowCloseButtonHint)

            self.setCentralWidget(self.stackedScreens)

            # Screens added in __init__, directly in screens
            for _, value in self.screens.items():
                self.stackedScreens.addWidget(value)

        cls.__init__ = newInit

        def addScreen(self, screen: QWidget):
            """
            Adds a screen widget to the main window's stacked widget.

            This method checks that the screen has a valid 'screenName' attribute and adds it 
            to the stacked widget for navigation.

            Args:
                screen (QWidget): The screen widget to add to the stacked widget.

            Raises:
                Exception: If the screen does not have a 'screenName' attribute.
            """
            if not hasattr(self, 'screens'):
                self.screens = {}

            # Added to dictionary
            name = screen.screenName
            self.screens[name] = screen
            
            if not hasattr(screen, 'name'):
                raise Exception(f"'The screen {screen}' does not have name <name>.")
            if not hasattr(screen, 'screenName'):
                raise Exception(f"'The screen {screen}' does not have name <screenName>.")
            
            if hasattr(self, 'stackedScreens'):
                # If the screen already exists, do not duplicate it
                self.stackedScreens.addWidget(screen)

        def setScreen(self, name: str) -> None:
            """
            Sets the current screen to display based on the screen name.

            This method accepts a string name that must match the 'screenName' attribute
            of a previously added screen.

            Args:
                name (str): The name of the screen to display.

            Raises:
                Exception: If the specified screen does not exist.
            """
            if name in self.screens:
                if hasattr(self, 'stackedScreens'):
                    currentScreen = self.stackedScreens.currentWidget()
                    if currentScreen:
                        self.screenHistory.append(currentScreen)

                    self.stackedScreens.setCurrentWidget(self.screens[name])      
            else:
                raise Exception(f"The screen '{name}' does not exist.")

        def createWindow(self, window: QMainWindow) -> None:
            """
            Creates a new window and adds it to the windows dictionary for management.

            The window is created using the attributes 'windowGeometry', 'title', and 'name' 
            of the specified QMainWindow instance.

            Args:
                window (QMainWindow): The window to create.

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
                window.closeEvent = lambda event: onWindowClose(self, event, name)
                self.windows[name] = window
                window.setGeometry(*geometry)
                window.setWindowTitle(title)

                if hasattr(window, '__effect__'):
                    window.__effect__()

                window.show()
            else:
                if QFlowDevConfiguration.USE_CONSOLE:         
                    print(f"The window '{name}' is already exist.")

        def onWindowClose(self, event, name):
            """
            Handles the window close event and removes the window from the windows list.

            Args:
                event: The close event.
                name (str): The name of the window being closed.
            """
            windowParent = self.windows[name]
            if windowParent.strictClosingWindows:
                for _, window in windowParent.windows.items():
                    window.close()

            QTimer.singleShot(0, lambda: removeWindow(self, name))
            event.accept()

        def removeWindow(self, name) -> None:
            """
            Removes a window from the windows list.

            Args:
                name (str): The name of the window to remove.
            """
            if name in self.windows:
                del self.windows[name]

        def setWindow(self, name: str) -> None:
            """
            Brings a specified window to the front and activates it.

            Args:
                name (str): The name of the window to bring to the front.

            Raises:
                Exception: If the specified window does not exist.
            """
            if name in self.windows:
                self.windows[name].raise_()
                self.windows[name].activateWindow()
            else:
                raise Exception(f"The window '{name}' does not exist.")

        def goBack(self) -> None:
            """
            Navigates back to the previous screen in the screen history.
            """
            if self.screenHistory:
                previousScreen = self.screenHistory.pop()
                self.stackedScreens.setCurrentWidget(previousScreen)

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
            Removes a screes from the screens list.

            Args:
                name (str): The name of the screen to remove.
            """
            if not self.screens[name]:
                raise Exception(f"The window '{name}' does not exist.")
            
            if hasattr(self, 'stackedScreens'):
                self.stackedScreens.removeWidget(self.screens[name])
            
            self.screens.pop(name)
        
        def existScreen(self, name: str) -> bool:
            """
            Checks if a screen exists in a window.

            Args:
                name (str): The name of the screen.
            Returns:
                exist (bool): True if the screen exists, false if it does not exist.
            """
            return name in self.screens
        
        def existWindow(self, name: str) -> bool:
            """
            Checks if a window exists in the main window.

            Args:
                name (str): The name of the window.
            Returns:
                exist (bool): True if the window exists, false if it does not exist.
            """
            return name in self.windows

        def reloadWindowScreens(self, window: str) -> None:
            """
            Reloads the screens of a window.

            Args:
                window (str): The name of the window to reload.
            """
            window: WindowTyping = self.windows[window] if window in self.windows else False
            if window:
                window.reloadScreens()
        
        def reloadWindowScreen(self, window: str, screen: str) -> None:
            """
            Reloads a screen of a window.

            Args:
                window (str): The name of the window to reload.
                screen (str): The name of the screen to reload.
            """
            window: WindowTyping = self.windows[window] if window in self.windows else False
            if window:
                window.reloadScreen(screen)

        def reloadScreens(self) -> None:
            """
            Reloads all window screens.
            """
            for name, screen in self.screens.items():
                screen: ScreenTyping
                if existScreen(self, name):
                    screen.reloadUI()
        
        def reloadScreen(self, name: str) -> None:
            """
            Reloads a screen of a specific window.

            Args:
                name (str): The name of the screen to reload.
            """
            if existScreen(self, name):
                screen: ScreenTyping = self.screens[name]
                screen.reloadUI()

        def onAppClose(self, event):
            if self.strictClosingWindows:
                for _, window in self.windows.items():
                    window.close()

            event.accept()
            
        cls.addScreen = addScreen
        cls.setScreen = setScreen
        cls.createWindow = createWindow
        cls.setWindow = setWindow
        cls.closeWindow = closeWindow
        cls.onWindowClose = onWindowClose
        cls.removeScreen = removeScreen
        cls.existScreen = existScreen
        cls.closeEvent = onAppClose
        cls.removeWindow = removeWindow
        cls.reloadWindowScreens = reloadWindowScreens
        cls.reloadWindowScreen = reloadWindowScreen
        cls.reloadScreens = reloadScreens
        cls.reloadScreen = reloadScreen
        cls.existWindow = existWindow
        cls.goBack = goBack

        return cls
    
    return decorator