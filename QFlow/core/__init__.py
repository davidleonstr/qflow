"""
# Core is intended for basic internal package compatibility.
## You can use it if you want basic compatibility between Qt frameworks.
Core exposes everything from: `QtWidgets`, `QtCore` and `QtGui`.
It exposes custom classes for managing modules that did not exist in previous versions and were necessary for the development of some sections.

`xQt`, `xQEvent`: Designed for internal management of some compatible components.
``

Compatibility module for PyQt and PySide support.

This module provides a unified interface for both PyQt and PySide frameworks,
allowing QFlow to work with either framework seamlessly.
"""

from .detection import getQtFramework, isPyqt, isPyside, getQtVersion, getAvailableFrameworks
from .imports import *
from .compatibility import xQt, xQEvent
from .config import QFlowDevConfiguration

__all__ = [
    # Widgets
    'QWidget', 'QMainWindow', 'QStackedWidget', 'QLabel', 'QVBoxLayout', 
    'QHBoxLayout', 'QPushButton', 'QLineEdit', 'QProgressBar', 'QFrame',
    
    # Core
    'QTimer', 'Qt', 'QEvent', 'QPropertyAnimation', 'pyqtProperty', 'xQt', 'xQEvent',
    
    # GUI
    'QIcon', 'QPixmap', 'QColor', 'QPainter', 'QBrush',
    
    # Framework detection
    'getQtFramework', 'isPyqt', 'isPyside', 'getQtVersion', 'getAvailableFrameworks',

    #Config
    'QFlowDevConfiguration'
]