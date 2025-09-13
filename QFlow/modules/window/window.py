"""
This module defines a decorator that assigns window properties and screen management capabilities
to a class.
"""

from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QStackedWidget, QWidget
from qtpy.QtCore import QTimer, Qt, QEvent
from typing import Dict
from typing import Callable
from ..screen import ScreenTyping
from .typing import WindowTyping, QMainWindow

def window(
        name: str, 
        title: str, 
        geometry: list[int], 
        icon: Callable[[], QIcon], 
        parentType = None,
        resizable: bool = True,
        strictClosingWindows: bool = True,
        opacity: float = 1.0,
        animatedEvents: Dict[str, bool] = {},
        animationValues: Dict[str, float] = {}
    ):
    """
    A decorator that assigns window properties and screen management capabilities to a class.

    This decorator allows you to configure the title, geometry, and icon of a window,
    while also providing built-in screen management functionality.

    Args:
        name (str): The name of the window.
        title (str): The title of the window.
        geometry (list): The geometry of the window (ax: int, ay: int, aw: int, ah: int).
        icon (QIcon): Callable to make the icon to set for the window.
        resizable (bool, optional): The ability to resize the window. Defaults to True.
        strictClosingWindows (bool, optional): Determines whether all windows should be closed when the window is closed. Defaults to True.
        opacity: (float, optional): The opacity of the window.
        animatedEvents: (Dict[str, bool], optional): Default animations for events to {'fadeIn': False, 'fadeOut': False}.
        animationValues: (Dict[str, bool], optional): Default values for animations {'opacityIncreasedIn': 0.02, 'opacityReductionOut': 0.02}.
    """
    def decorator(cls):
        """
        A decorator that assigns window properties and screen management.

        Args:
            cls (type): The class to be decorated.

        Returns:
            type: The decorated class with window properties and screen management.
        """
        originalInit = cls.__init__

        def newInit(self, *args, **kwargs):
            """
            Initializes the decorated class with window settings and screen management.

            This method initializes window properties and screen management attributes
            before calling the original __init__ method to ensure all required attributes
            are available when needed.

            Args:
                *args: Positional arguments passed to the original class initializer.
                **kwargs: Keyword arguments passed to the original class initializer.
            """
            # Initialize window properties first
            self.name = name
            self.title = title
            self.windowGeometry = geometry
            self.icon = icon
            
            # Initialize screen management
            self.screenHistory = []
            self.screens = {}  # Initialize screens dictionary
            self.stackedScreens = QStackedWidget()  # Initialize stacked widget
            self.windows = {}
            self.strictClosingWindows = strictClosingWindows

            self.msRenderTime = 16
            
            # Initialize parent class
            originalInit(self, *args, **kwargs)
            
            # Configure window
            self.setWindowTitle(self.title)
            self.setGeometry(*self.windowGeometry)

            if not resizable:
                ah, aw = geometry[-2:]
                self.setFixedSize(ah, aw)

            self.setWindowIcon(icon())
            self.setCentralWidget(self.stackedScreens)  # Set central widget

            if opacity != 1.0:
                self.setWindowOpacity(opacity)

            self.opacity = opacity

            self._animationValues = {
                'opacityIncreasedIn': 0.02,
                'opacityReductionOut': 0.02
            }
            self._animationValues.update(animationValues)

            self._animatedEvents = {
                'fadeIn': False,
                'fadeOut': False
            }
            self._animatedEvents.update(animatedEvents)

            parent = self.parent()

            if parentType is not None:
                if parent.__class__.__bases__[0] != parentType:
                    raise TypeError(
                        f"Window '{name}' only accepts the parentType '{parentType}' not '{parent.__class__.__bases__[0]}'"
                    )

        def addScreen(self, screen: QWidget):
            """
            Adds a screen widget to the window's stacked widget.

            This method checks that the screen has a valid 'name' attribute and adds it 
            to the stacked widget for navigation.

            Args:
                screen (QWidget): The screen widget to add to the stacked widget.

            Raises:
                Exception: If the screen does not have a 'name' attribute.
            """
            if not hasattr(screen, 'screenName'):
                raise Exception(f'{screen} does not have screenName attribute.')
            
            name = screen.screenName
            self.screens[name] = screen
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
                currentScreen = self.stackedScreens.currentWidget()
                if currentScreen:
                    self.screenHistory.append(currentScreen)

                screen = self.screens[name]
                if not hasattr(screen, 'screenName'):
                    raise Exception(f'The screen {screen} does not have screenName attribute.')
                
                self.stackedScreens.setCurrentWidget(screen)      
            else:
                raise Exception(f'The screen window does not exist {name}.')
            
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
                raise ValueError("Window name must be a non-empty string")
            
            self.name = name
        
        def _animateFadeOut(self) -> None:
            timer = QTimer(self)
            opacity = self.windowOpacity()

            def _modifyOpacity():
                nonlocal opacity
                opacity -= self._animationValues['opacityReductionOut']

                if opacity <= 0.2:
                    timer.stop()
                    
                self.setWindowOpacity(opacity)

            timer.timeout.connect(_modifyOpacity)
            timer.start(self.msRenderTime)

        def _animateFadeIn(self) -> None:
            if not self._animatedEvents['fadeOut']:
                self.setWindowOpacity(0.2)

            timer = QTimer(self)
            opacity = self.windowOpacity()

            def _modifyOpacity():
                nonlocal opacity
                opacity += self._animationValues['opacityIncreasedIn']

                if opacity >= self.opacity:
                    timer.stop()
                    
                self.setWindowOpacity(opacity)

            timer.timeout.connect(_modifyOpacity)
            timer.start(self.msRenderTime)

        def changeEvent(self, event):
            if event.type() == QEvent.Type.WindowStateChange:
                if self.windowState() == Qt.WindowState.WindowMinimized:
                    if self._animatedEvents['fadeOut']:
                        _animateFadeOut(self)
                elif self.windowState() == Qt.WindowState.WindowNoState:
                    if self._animatedEvents['fadeIn']:
                        _animateFadeIn(self)
                    else:
                        self.setWindowOpacity(self.opacity)

        def existScreen(self, name: str) -> bool:
            """
            Checks if a screen exists in a window.

            Args:
                name (str): The name of the window.
            Returns:
                exist (bool): True if the screen exists, false if it does not exist.
            """
            return name in self.screens

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
                print(f"The window '{name}' is already exist.")

        def onWindowClose(self, event, name):
            """
            Handles the window close event and removes the window from the windows list.

            Args:
                event: The close event.
                name (str): The name of the window being closed.
            """
            if self.strictClosingWindows:
                for _, window in self.windows.items():
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

        cls.__init__ = newInit

        # Add instance methods
        cls.addScreen = addScreen
        cls.setScreen = setScreen
        cls.goBack = goBack
        cls.setWindowName = setWindowName
        cls.existScreen = existScreen
        cls.reloadScreens = reloadScreens
        cls.removeScreen = removeScreen
        cls.reloadScreen = reloadScreen
        cls.createWindow = createWindow
        cls.setWindow = setWindow
        cls.closeWindow = closeWindow
        cls.onWindowClose = onWindowClose
        cls.removeWindow = removeWindow
        cls.reloadWindowScreens = reloadWindowScreens
        cls.reloadWindowScreen = reloadWindowScreen
        cls.existWindow = existWindow

        if animatedEvents is not None:
            cls.changeEvent = changeEvent

        return cls

    return decorator