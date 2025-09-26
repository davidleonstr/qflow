from __future__ import annotations
"""
This module defines a Window class that provides window properties and screen management capabilities.
"""

from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QStackedWidget, QWidget, QMainWindow
from qtpy.QtCore import QTimer, Qt, QEvent
from typing import Dict, Callable
from ...core.temp import INSTANCE_ARGS

class Window(QMainWindow):
    """
    A window class that provides window properties and screen management capabilities.

    This class allows you to configure the title, geometry, and icon of a window,
    while also providing built-in screen management functionality.
    """
    
    def __init__(
        self,
        name: str = '',
        title: str = '',
        geometry: list[int] = [],
        maximizable=True,
        icon: Callable[[], QIcon] = [],
        parent=None,
        parentType=None,
        resizable: bool = True,
        strictClosingWindows: bool = True,
        opacity: float = 1.0,
        animatedEvents: Dict[str, bool] = None,
        animationValues: Dict[str, float] = None
    ):
        """
        Initializes the Window with specified properties and screen management.

        Args:
            name (str): The name of the window.
            title (str): The title of the window.
            geometry (list): The geometry of the window (ax: int, ay: int, aw: int, ah: int).
            maximizable (bool, optional): Determines whether the window can be maximized. Defaults to True.
            icon (Callable[[], QIcon]): Callable to make the icon to set for the window.
            parent: Parent widget.
            parentType: Expected parent type for validation.
            resizable (bool, optional): The ability to resize the window. Defaults to True.
            strictClosingWindows (bool, optional): Determines whether all windows should be closed when the window is closed. Defaults to True.
            opacity (float, optional): The opacity of the window.
            animatedEvents (Dict[str, bool], optional): Default animations for events to {'fadeIn': False, 'fadeOut': False}.
            animationValues (Dict[str, float], optional): Default values for animations {'opacityIncreasedIn': 0.02, 'opacityReductionOut': 0.02}.
        """
        super().__init__(parent)
        
        # Initialize window properties
        self.name = name
        self.title = title
        self.windowGeometry = geometry
        self.icon = icon

        self.args = {}
        """
        Dictionary with the arguments passed from the window decorator.
        """
        
        # Initialize screen management
        self.screenHistory = []
        self.screens = {}
        self.stackedScreens = QStackedWidget()
        self.windows = {}
        self.strictClosingWindows = strictClosingWindows
        self.msRenderTime = 16
        
        # Configure window
        self.setWindowTitle(self.title)
        self.setGeometry(*self.windowGeometry)

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

        self.setWindowIcon(icon())
        self.setCentralWidget(self.stackedScreens)

        if opacity != 1.0:
            self.setWindowOpacity(opacity)

        self.opacity = opacity

        # Initialize animation settings
        self._animationValues = {
            'opacityIncreasedIn': 0.02,
            'opacityReductionOut': 0.02
        }
        if animationValues:
            self._animationValues.update(animationValues)

        self._animatedEvents = {
            'fadeIn': False,
            'fadeOut': False
        }
        if animatedEvents:
            self._animatedEvents.update(animatedEvents)

        # Validate parent type if specified
        if parentType is not None and parent is not None:
            if type(parent) != parentType:
                raise TypeError(
                    f"Window '{name}' only accepts the parentType '{parentType}' not '{type(parent)}'"
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
            raise Exception(f'{screen} does not have screenName attribute.')
        
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
                raise Exception(f'The screen `{screen}` does not have screenName attribute.')
            
            if args:
                INSTANCE_ARGS.setArgs(instance=screen, args=args)
            
            self.stackedScreens.setCurrentWidget(screen)      
        else:
            raise Exception(f'The screen `{name}` does not exist.')
            
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
        """
        Animates the window fade out effect.
        """
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
        """
        Animates the window fade in effect.
        """
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
        """
        Handles window state change events for animations.
        
        Args:
            event: The change event.
        """
        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() == Qt.WindowState.WindowMinimized:
                if self._animatedEvents['fadeOut']:
                    self._animateFadeOut()
            elif self.windowState() == Qt.WindowState.WindowNoState:
                if self._animatedEvents['fadeIn']:
                    self._animateFadeIn()
                else:
                    self.setWindowOpacity(self.opacity)

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

    def createWindow(self, window: "Window") -> None:
        """
        Creates a new window and adds it to the windows dictionary for management.

        The window is created using the attributes 'windowGeometry', 'title', and 'name' 
        of the specified Window instance.

        Args:
            window (Window): The window to create.

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

            if hasattr(window, '__effect__'):
                window.__effect__()

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
            for _, window in self.windows.items():
                window.close()

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