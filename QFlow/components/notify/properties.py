"""
This file contains the constants and properties for the Notify object in this module.

Modifying any property in this file requires making the same changes in related files.
"""

import importlib.resources as res
import QFlow

# Class for creating Pixmap icons
from ...helpers.icon import Icon

# Location of the file with the styles for the Notify object
STYLE_PATH = str(res.files(QFlow).joinpath('components/notify/notify.css'))
"""Path to the file containing the styles for the Notify object."""

# References to create the default icons of the Notify class
ICONS = {
    'success': lambda: Icon(str(res.files(QFlow).joinpath('components/notify/icons/check.png')), 25, 25),
    'error': lambda: Icon(str(res.files(QFlow).joinpath('components/notify/icons/close.png')), 25, 25),
    'info': lambda: Icon(str(res.files(QFlow).joinpath('components/notify/icons/information.png')), 25, 25),
}
"""
Dictionary mapping notification types to their default icons.

Available types:
- **success** → Green check icon.
- **error** → Red close icon.
- **info** → Blue information icon.
"""

# Object names for each style
STYLE_THEME_COLOR = {
    'black': {
        'QFrame': 'black-QFrame',
        'QLabel': 'white-QLabel',
    },
    'white': {
        'QFrame': 'white-QFrame',
        'QLabel': 'black-QLabel',
    },
}
"""
Dictionary defining object names for each style.

Available styles:
- **black** → Black frame with white labels.
- **white** → White frame with black labels.
"""

# Object names to change the color of the progress bar in the Notify class
STYLE_BAR = {
    'success': 'success-QProgressBar',
    'error': 'error-QProgressBar',
    'info': 'info-QProgressBar',
}
"""
Dictionary defining the object names for changing the Notify progress bar color.

Available types:
- **success** → Green progress bar.
- **error** → Red progress bar.
- **info** → Blue progress bar.
"""