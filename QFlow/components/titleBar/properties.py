"""
This file contains the constants and properties for the TitleBar object in this module.

Modifying any property in this file requires making the same changes in related files.
"""

from ...utils import Source

# Importamos QIcon para que Qt lo reconozca nativamente
from qtpy.QtGui import QIcon

# Class for creating Pixmap icons
from ...helpers.icon import Icon

from ...core.flags import FROZENLIB

# Location of the file with the styles for the titleBar object
STYLE_PATH = Source('QFlow/components/titleBar/titleBar.qss', frozen=FROZENLIB).get()
"""Path to the file containing the styles for the titleBar object."""

# References to create the default icons of the titleBar class
ICONS = {
    'close': lambda: QIcon(Icon(
        Source('QFlow/components/titleBar/icons/close.png', frozen=FROZENLIB).get(), 
        25, 25
    )),
    'minimize': lambda: QIcon(Icon(
        Source('QFlow/components/titleBar/icons/minimize.png', frozen=FROZENLIB).get(), 
        25, 25
    )),
    'maximize-default': lambda: QIcon(Icon(
        Source('QFlow/components/titleBar/icons/maximize-default.png', frozen=FROZENLIB).get(), 
    25, 25)),
    'maximize-minimize': lambda: QIcon(Icon(
        Source('QFlow/components/titleBar/icons/maximize-minimize.png', frozen=FROZENLIB).get(), 
    25, 25))
}