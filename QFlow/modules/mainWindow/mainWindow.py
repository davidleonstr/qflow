"""
This module defines a decorator that can be used to create a main window with support for
multiple screens and window management.

The mainWindow decorator allows for setting a window title, geometry, and icon. It provides 
functionality to manage a stack of screens, add new screens, and create and manage separate 
windows for each screen.
"""

from PyQt5.QtWidgets import QWidget, QStackedWidget, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt

def mainWindow(
        title: str, 
        geometry: list[int], 
        icon: QIcon, 
        resizable: bool = True, 
        maximizable: bool = True
    ):
    """
    A decorator that adds window management functionality to a class.

    This decorator creates a main window with support for multiple screens and window handling.
    It allows setting a window title, geometry, and icon, and provides methods for switching 
    screens, creating windows for each screen, and managing window history.

    Args:
        title (str): The title to set for the window.
        geometry (list): The window geometry as a list [x, y, width, height].
        icon (QIcon): The icon to set for the window.
        resizable (bool, optional): Determines whether the window can be resized. Defaults to True.
        maximizable (bool, optional): Determines whether the window can be maximized. Defaults to True.
    
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
            originalInit(self, *args, **kwargs)

            self.setWindowTitle(title)
            self.setGeometry(*geometry)
            self.setWindowIcon(icon)

            if not resizable:
                ah, aw = self.windowGeometry[-2:]
                self.setFixedSize(ah, aw)
                self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
            
            if not maximizable:
                self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

            self.screenHistory = []  # Stores the history of screens navigated back to.

            self.stackedScreens = QStackedWidget()
            self.setCentralWidget(self.stackedScreens)

            for _, value in cls.screens.items():
                self.stackedScreens.addWidget(value)

        cls.__init__ = newInit

        @staticmethod
        def addScreen(screen: QWidget):
            """
            Adds a screen widget to the main window's stacked widget.

            This method checks that the screen has a valid 'screenName' attribute and adds it 
            to the stacked widget for navigation.

            Args:
                screen (QWidget): The screen widget to add to the stacked widget.

            Raises:
                Exception: If the screen does not have a 'screenName' attribute.
            """
            if not hasattr(cls, 'screens'):
                cls.screens = {}

            name = screen.screenName
            cls.screens[name] = screen
            
            if not hasattr(screen, 'name'):
                raise Exception(f'{screen} does not have name <name>.')
            
            if hasattr(cls, 'stackedScreens'):
                cls.stackedScreens.addWidget(screen)

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
                raise Exception(f'The screen window does not exist {name}.')

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
            # Validar y obtener atributos con 'getattr'
            geometry = getattr(window, 'windowGeometry', None)
            title = getattr(window, 'title', None)
            name = getattr(window, 'name', None)

            if not geometry:
                raise Exception(f'{window} does not have a valid <windowGeometry>.')
            if not title:
                raise Exception(f'{window} does not have a valid <title>.')
            if not name:
                raise Exception(f'{window} does not have a valid <name>.')

            # Inicializar diccionario de ventanas si no existe
            if not hasattr(self, 'windows'):
                self.windows = {}

            if not self.windows.get(name):
                # Configurar ventana y mostrarla
                window.closeEvent = lambda event: onWindowClose(event, name)
                self.windows[name] = window
                window.setGeometry(*geometry)
                window.setWindowTitle(title)
                window.show()
            else:
                print(f'Window {name} is already exist.')

        @staticmethod
        def onWindowClose(event, name):
            """
            Handles the window close event and removes the window from the windows list.

            Args:
                event: The close event.
                name (str): The name of the window being closed.
            """
            QTimer.singleShot(0, lambda: removeWindow(name))
            event.accept()

        @staticmethod
        def removeWindow(name) -> None:
            """
            Removes a window from the windows list.

            Args:
                name (str): The name of the window to remove.
            """
            if name in cls.windows:
                del cls.windows[name]

        @staticmethod
        def setWindow(name: str) -> None:
            """
            Brings a specified window to the front and activates it.

            Args:
                name (str): The name of the window to bring to the front.

            Raises:
                Exception: If the specified window does not exist.
            """
            if name in cls.windows:
                cls.windows[name].raise_()
                cls.windows[name].activateWindow()
            else:
                raise Exception(f'The window {name} does not exist.')

        def goBack(self) -> None:
            """
            Navigates back to the previous screen in the screen history.
            """
            if self.screenHistory:
                previousScreen = self.screenHistory.pop()
                self.stackedScreens.setCurrentWidget(previousScreen)

        @staticmethod
        def closeWindow(name: str) -> None:
            """
            Closes a specified window.

            Args:
                name (str): The name of the window to close.

            Raises:
                Exception: If the specified window does not exist.
            """
            if name in cls.windows:
                cls.windows[name].close()
                del cls.windows[name]
            else:
                raise Exception(f'The window {name} does not exist.')

        cls.title = title
        cls.windowGeometry = geometry
        cls.icon = icon
        cls.addScreen = addScreen
        cls.setScreen = setScreen
        cls.createWindow = createWindow
        cls.setWindow = setWindow
        cls.closeWindow = closeWindow
        cls.onWindowClose = onWindowClose
        cls.goBack = goBack
        cls.screens = {}
        cls.windows = {}

        return cls
    
    return decorator