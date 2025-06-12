"""
This module defines the Dialog class, which represents a floating dialog window in a PyQt5 application.

The class provides a customizable modal-like dialog with an optional backdrop.
It supports adding child layouts or individual widgets dynamically.
A decorator is used to apply styles from an external file.
"""

from PyQt5.QtWidgets import (
    QVBoxLayout, QFrame, QHBoxLayout, QWidget
)
from .properties import STYLE_PATH, STYLE_THEME_COLOR
from ...modules.style import style


@style(STYLE_PATH, True)
class Dialog(QFrame):
    """
    Represents a floating dialog window.

    This class creates a centered pop-up dialog with an optional backdrop.
    It supports adding widgets dynamically and adjusting its size.
    """

    def __init__(
            self, 
            parent, 
            childrenLayout: QVBoxLayout | QHBoxLayout = None, 
            color: str = 'white', 
            fixedSize: list[int] = [300, 200],
            backdrop: str = 'background-color: rgba(0, 0, 0, 0.5);'
        ):
        """
        Initializes a Dialog object.

        Args:
            parent (QWidget): The parent widget where the dialog will appear. It's usually the window.
            childrenLayout (QVBoxLayout | QHBoxLayout, optional): The layout to add as children. Default is None.
            color (str, optional): The theme color. Default is 'white'.
            fixedSize (list, optional): The fixed size of the dialog [width, height]. Default is [300, 200].
            backdrop (str, optional): CSS style for the backdrop overlay. Default is a semi-transparent black.
        """

        super().__init__(parent)

        self.setObjectName(STYLE_THEME_COLOR[color]['floatingDialog'])
        
        self.backdrop = QFrame(parent)
        self.backdrop.setStyleSheet(backdrop)
        self.backdrop.setGeometry(0, 0, parent.width(), parent.height())

        self.backdrop.hide()

        self.backdrop.mousePressEvent = self.close

        self.childrenLayout = childrenLayout
        self.fixedSize = fixedSize

        self.setFixedSize(*self.fixedSize)

        self.mainLayout = QVBoxLayout(self)

        if self.childrenLayout is not None:
            self.mainLayout.addLayout(self.childrenLayout)

        self.hide()
    
    def addWidget(self, widget: QWidget) -> None:
        """
        Adds a widget to the dialog.

        Args:
            widget (QWidget): The widget to add to the dialog.
        """

        self.mainLayout.addWidget(widget)

    def addLayout(self, layout: QHBoxLayout | QVBoxLayout) -> None:
        """
        Adds a layout to the dialog.

        Args:
            layout (QHBoxLayout | QVBoxLayout): The layout to add to the dialog.
        """

        self.mainLayout.addLayout(layout)

    def show(self) -> None:
        """
        Displays the dialog, centering it relative to its parent.
        """

        if self.parent():
            w, h = self.parent().width(), self.parent().height()
            self.move((w - self.width()) // 2, (h - self.height()) // 2)
            self.backdrop.setGeometry(0, 0, w, h)

        self.backdrop.show()
        self.backdrop.raise_()
        self.raise_()
        super().show()

    # Close uses event, but doesn't need it
    def close(self, event=None) -> None:
        """
        Closes the dialog and hides the backdrop.
        """
        self.backdrop.hide()
        self.hide()