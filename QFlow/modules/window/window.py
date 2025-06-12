"""
This module defines a decorator that assigns window properties and screen management capabilities
to a class.
   
The decorator initializes window properties and screen management attributes before calling
the original __init__ method to ensure all required attributes are available when needed.
"""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStackedWidget, QWidget
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtCore import QTimer
from typing import Dict

def window(
        name: str, 
        title: str, 
        geometry: list[int], 
        icon: QIcon, 
        resizable: bool = True,
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
        icon (QIcon): The icon of the window.
        resizable (bool, optional): The ability to resize the window. Defaults to True.
        opacity: (float, optional): The opacity of the window.
        animatedEvents: (Dict[str, bool], optional): Default animations for events to {'fadeIn': False, 'fadeOut': False}.
        animationValues: (Dict[str, bool], optional): Default values for animations {'opacityIncreasedIn': 0.02, 'opacityReductionOut': 0.02}.
    
    Returns:
        function: A decorator that adds the following to the decorated class:
            - Window properties (name, title, geometry, icon)
            - Screen management attributes (screenHistory, screens, stackedScreens)
            - `addScreen(screen)` method: Adds a screen to the window
            - `setScreen(name)` method: Sets the current screen
            - `goBack()` method: Navigates back to the previous screen
            - `setWindowName(name)` method: Changes the window name
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
            
            # Initialize screen management
            self.screenHistory = []
            self.screens = {}  # Initialize screens dictionary
            self.stackedScreens = QStackedWidget()  # Initialize stacked widget
            
            # Initialize parent class
            originalInit(self, *args, **kwargs)
            
            # Configure window
            self.setWindowTitle(self.title)
            self.setGeometry(*self.windowGeometry)

            if not resizable:
                ah, aw = geometry[-2:]
                self.setFixedSize(ah, aw)

            self.setWindowIcon(icon)
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

            self.msRenderTime = 16

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
            if event.type() == QEvent.WindowStateChange:
                if self.windowState() == Qt.WindowMinimized:
                    if self._animatedEvents['fadeOut']:
                        _animateFadeOut(self)
                elif self.windowState() == Qt.WindowNoState:
                    if self._animatedEvents['fadeIn']:
                        _animateFadeIn(self)
                    else:
                        self.setWindowOpacity(self.opacity)

        cls.__init__ = newInit

        # Add instance methods
        cls.addScreen = addScreen
        cls.setScreen = setScreen
        cls.goBack = goBack
        cls.setWindowName = setWindowName

        if animatedEvents is not None:
            cls.changeEvent = changeEvent

        return cls

    return decorator