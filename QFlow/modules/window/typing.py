from PyQt5.QtWidgets import QWidget, QStackedWidget, QMainWindow
from PyQt5.QtGui import QIcon
from typing import Protocol
from typing import Dict, List

class WindowTyping(Protocol):
    """
    # Includes self-typing of Qurderer MainScreen.
    """
    name: str
    title: str
    windowGeometry: List
    icon: QIcon
    screenHistory: List[str]
    stackedScreens: QStackedWidget
    screens: Dict[str, QWidget]
    opacityIncreasedIn: bool
    opacityReductionOut: bool

    def setScreen(self, screen: QWidget) -> None: ...
    def addScreen(self, screen: QWidget) -> None: ...
    def setWindowName(self, name: str) -> None: ...
    def goBack(self) -> None: ...

class Window(QMainWindow):
    """
    # All attributes and methods can be used directly from self. This class is intended for typing using cls only.

    Attributes:
        cls (WindowTyping): A type-casted version of self for use in autocompletion tools.
    
    Inherited class of PyQt5 QMainWindow used for typing.

    Not required, recommended use only for developers with good knowledge of the package.
    """
    @property
    def cls(self) -> WindowTyping:
        return self