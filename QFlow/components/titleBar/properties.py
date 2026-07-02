"""
This file contains the constants and properties for the TitleBar object in this module.

Modifying any property in this file requires making the same changes in related files.
"""

from QFlow.utils import Source

# Importamos QIcon para que Qt lo reconozca nativamente
from qtpy.QtGui import QIcon

# Class for creating Pixmap icons
from QFlow.builders import Icon

# Location of the file with the styles for the titleBar object
STYLEPATH = Source.library(r'QFlow/components/titleBar/titleBar.qss').get()
"""Path to the file containing the styles for the titleBar object."""

# References to create the default icons of the titleBar class
ICONS = {
    'close': lambda: QIcon(Icon(
        Source.library(r'QFlow/components/titleBar/icons/close.png').get(), 
        25, 25
    )),
    'minimize': lambda: QIcon(Icon(
        Source.library(r'QFlow/components/titleBar/icons/minimize.png').get(), 
        25, 25
    )),
    'maximize-default': lambda: QIcon(Icon(
        Source.library(r'QFlow/components/titleBar/icons/maximize-default.png').get(), 
    25, 25)),
    'maximize-minimize': lambda: QIcon(Icon(
        Source.library(r'QFlow/components/titleBar/icons/maximize-minimize.png').get(), 
    25, 25))
}