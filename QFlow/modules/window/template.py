from qtpy.QtWidgets import QWidget
from .window import Window
from typing import Callable

class Template(QWidget):
    """
    A class that represents a custom template for screens; its main characteristic is having a parent Window.
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.parent: Callable[[], Window] = lambda: parent