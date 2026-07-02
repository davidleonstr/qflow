from dataclasses import dataclass, field
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QWidget
from typing import Callable

@dataclass
class WindowParams:
    name: str = ''
    title: str = ''
    geometry: list[int] = field(default_factory=list)
    maximizable: bool = True
    resizable: bool = True
    strictClosingWindows: bool = True
    opacity: float = 1.0
    frameless: bool = False
    icon: Callable[[], QIcon] = None
    customTemplate: Callable[[], QWidget] = None
    parentType: type = None
    parent: QWidget = None