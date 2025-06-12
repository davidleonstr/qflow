from PyQt5.QtWidgets import QWidget
from typing import Protocol

class ScreenTyping(Protocol):
    """
    # Includes self-typing of Qurderer Screen.
    """
    name: str
    screenName: str

    def removeAllLayouts(widget: QWidget) -> None: ...
    def reloadUI(self) -> None: ...
    def setScreenName(self, name: str) -> None: ...

class Screen(QWidget):
    """
    # All attributes and methods can be used directly from self. This class is intended for typing using cls only.

    Attributes:
        cls (ScreenTyping): A type-casted version of self for use in autocompletion tools.
    
    Inherited class of PyQt5 QWidget used for typing.

    Not required, recommended use only for developers with good knowledge of the package.
    """
    @property
    def cls(self) -> ScreenTyping:
        return self