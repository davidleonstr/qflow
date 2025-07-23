from qtpy.QtWidgets import QWidget
from ..app.typing import AppTyping
from typing import Protocol

class ScreenTyping(Protocol):
    """
    # Includes self-typing of QFlow Screen.
    """
    name: str
    screenName: str

    def removeAllLayouts(widget: QWidget) -> None: ...
    def reloadUI(self) -> None: ...
    def setScreenName(self, name: str) -> None: ...
    def __effect__(self) -> None: ...
    def parent(self) -> AppTyping:
        """
        Outside of .typ, parent method still returns an App instance
        """
        ...

class Screen(QWidget):
    """
    # All attributes and methods can be used directly from self. This class is intended for typing using typ only.

    Attributes:
        typ (ScreenTyping): A type-casted version of self for use in autocompletion tools.
    
    Inherited class of PyQt5 QWidget used for typing.

    Not required, recommended use only for developers with good knowledge of the package.
    """
    @property
    def typ(self) -> ScreenTyping:
        """
        Property to access the class typing.
        """
        return self