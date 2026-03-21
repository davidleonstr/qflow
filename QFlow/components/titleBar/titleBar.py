"""
This module defines the TitleBar class, a custom window title bar 
for PyQt-PySide applications.

It provides basic window controls such as minimize, maximize, and close,
along with support for custom icons, styling, and event callbacks.
"""

from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from qtpy.QtCore import Qt
from typing import Callable
from ...modules.style import style
from .properties import STYLE_PATH, ICONS


@style(STYLE_PATH, True)
class TitleBar(QWidget):
    """
    Custom window title bar widget.

    This class replaces the default system title bar and provides
    customizable controls such as minimize, maximize, and close buttons.
    It also allows attaching custom callback functions to window events.
    """

    def __init__(
            self, 
            parent, 
            title: str, 
            icons: dict = ICONS,
            contentsMargins: list = [10, 0, 0, 0],
            spacing: int = 0,
            fixedHeight: int = 35,
            onWindowClose: Callable = lambda: (), 
            onWindowMinimize: Callable = lambda: (), 
            onWindowMaximize: Callable = lambda: ()
        ):
        """
        Initializes the TitleBar.

        Args:
            parent (QWidget): The parent window where the title bar is attached.
            title (str): The text displayed as the window title.
            icons (dict, optional): Dictionary containing icon factory functions. Defaults to ICONS.
            contentsMargins (list, optional): Layout margins [left, top, right, bottom]. Defaults to [10, 0, 0, 0].
            spacing (int, optional): Spacing between widgets in the layout. Defaults to 0.
            fixedHeight (int, optional): Fixed height of the title bar. Defaults to 35.
            onWindowClose (Callable, optional): Callback executed before closing the window.
            onWindowMinimize (Callable, optional): Callback executed before minimizing the window.
            onWindowMaximize (Callable, optional): Callback executed before maximizing/restoring the window.
        """
        super().__init__(parent)

        self.onWindowClose = onWindowClose
        self.onWindowMinimize = onWindowMinimize
        self.onWindowMaximize = onWindowMaximize

        self.icons = icons

        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(*contentsMargins)
        self.layout.setSpacing(spacing)
        self.setFixedHeight(fixedHeight)

        self.title = QLabel(title)
        self.title.setObjectName('titleBarTitle')
        
        self.btnMinimize = QPushButton(icon=self.icons.get('minimize')())
        self.btnMaximize = QPushButton(icon=self.icons.get('maximize-default')())
        self.btnClose = QPushButton(icon=self.icons.get('close')())

        self.btnClose.setObjectName('titleBarCloseBtn')
        self.btnMinimize.setObjectName('titleBarDefaultBtn')
        self.btnMaximize.setObjectName('titleBarDefaultBtn')

        self.btnMinimize.clicked.connect(self.minimize)
        self.btnMaximize.clicked.connect(self.maximize)
        self.btnClose.clicked.connect(self.close)

        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.btnMinimize)
        self.layout.addWidget(self.btnMaximize)
        self.layout.addWidget(self.btnClose)

        self.startPos = None

    def close(self):
        """
        Closes the parent window.

        This method first executes the custom `onWindowClose` callback,
        then closes the parent widget.
        """
        # Execute custom window close
        self.onWindowClose()

        # Close window
        self.parent.close()

    def minimize(self):
        """
        Minimizes the parent window.

        Executes the custom `onWindowMinimize` callback before minimizing.
        """
        # Execute custom window minimize
        self.onWindowMinimize()

        # Minimize window
        self.parent.showMinimized()

    def maximize(self):
        """
        Toggles between maximized and normal state.

        Executes the custom `onWindowMaximize` callback before changing state.
        Also updates the maximize button icon depending on the current state.
        """
        # Execute custom window maximize
        self.onWindowMaximize()

        if self.parent.isMaximized():
            self.parent.showNormal()
            self.btnMaximize.setIcon(self.icons.get('maximize-default')())
        else:
            self.parent.showMaximized()
            self.btnMaximize.setIcon(self.icons.get('maximize-minimize')())

    def mousePressEvent(self, event):
        """
        Handles mouse press events.

        Stores the initial mouse position when the left button is pressed,
        allowing the window to be dragged.
        """
        if event.button() == Qt.LeftButton:
            self.startPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """
        Handles mouse move events.

        Moves the parent window when dragging the title bar.
        """
        if self.startPos:
            delta = event.globalPosition().toPoint() - self.startPos
            self.parent.move(self.parent.pos() + delta)
            self.startPos = event.globalPosition().toPoint()