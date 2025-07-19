from ...core import QWidget, QStackedWidget, QMainWindow, QIcon
from typing import Protocol
from ..app.typing import AppTyping
from typing import Dict, List, Callable

class WindowTyping(Protocol):
    """
    # Includes self-typing of Qurderer MainScreen.
    """
    name: str
    title: str
    windowGeometry: List
    icon: Callable[[], QIcon]
    screenHistory: List[str]
    stackedScreens: QStackedWidget
    screens: Dict[str, QWidget]
    opacityIncreasedIn: bool
    opacityReductionOut: bool
    windows: Dict[str, QMainWindow]
    strictClosingWindows: bool

    def parent(self) -> AppTyping: 
        """
        Outside of .typ, parent method still returns an App instance
        """
        ...
    def setScreen(self, screen: QWidget) -> None: ...
    def addScreen(self, screen: QWidget) -> None: ...
    def removeWindow(self, name) -> None: ...
    def setWindowName(self, name: str) -> None: ...
    def goBack(self) -> None: ...
    def existScreen(self, name: str) -> bool: ...
    def reloadScreens(self) -> None: ...
    def reloadScreen(self, name: str) -> None: ...
    def setWindow(self, name: str) -> None: ...
    def createWindow(self, window: QMainWindow) -> None: ...
    def onWindowClose(self, event, name): ...
    def closeWindow(self, name) -> None: ...
    def reloadWindowScreens(self, windowName: str) -> None: ...
    def reloadWindowScreen(self, window: str, screen: str) -> None: ...
    def removeWindow(self, name) -> None: ...
    def existWindow(self, name: str) -> bool: ...
    def __effect__(self) -> None: ...

class Window(QMainWindow):
    """
    # All attributes and methods can be used directly from self. This class is intended for typing using typ only.

    Attributes:
        typ (WindowTyping): A type-casted version of self for use in autocompletion tools.
    
    Inherited class of PyQt/PySide QMainWindow used for typing.

    Not required, recommended use only for developers with good knowledge of the package.
    """
    @property
    def typ(self) -> WindowTyping:
        """
        Property to access the class typing.
        """
        return self