from PyQt5.QtWidgets import QWidget, QStackedWidget, QMainWindow
from PyQt5.QtGui import QIcon
from typing import Protocol
from typing import Dict, List

class MainWindowTyping(Protocol):
    """
    # Includes self-typing of Qurderer MainScreen.
    """
    title: str
    windowGeometry: List
    icon: QIcon
    screenHistory: List[str]
    stackedScreens: QStackedWidget
    screens: Dict[str, QWidget]
    windows: Dict[str, QMainWindow]

    def setScreen(self, screen: QWidget) -> None: ...
    def addScreen(self, screen: QWidget) -> None: ...
    def setWindow(name: str) -> None: ...
    def createWindow(self, window: QMainWindow) -> None: ...
    def closeWindow(name: str) -> None: ...
    def onWindowClose(event, name): ...
    def removeWindow(name) -> None: ...
    def goBack(self) -> None: ...

class MainWindow(QMainWindow):
    """
    # All attributes and methods can be used directly from self. This class is intended for typing using cls only.

    Attributes:
        cls (MainWindowTyping): A type-casted version of self for use in autocompletion tools.
    
    Inherited class of PyQt5 QMainWindow used for typing.

    Not required, recommended use only for developers with good knowledge of the package.
    """
    @property
    def cls(self) -> MainWindowTyping:
        return self