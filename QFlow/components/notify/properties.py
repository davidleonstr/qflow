"""
This file contains the constants and properties for the Notify object in this module.

Modifying any property in this file requires making the same changes in related files.
"""

from ...utils import Source

# Class for creating Pixmap icons
from ...helpers.icon import Icon

from ...core.flags import FROZEN_LIB

# Location of the file with the styles for the Notify object
STYLE_PATH = Source('QFlow/components/notify/notify.css', frozen=FROZEN_LIB).get()
"""Path to the file containing the styles for the Notify object."""

# References to create the default icons of the Notify class
ICONS = {
    'success': lambda: Icon(
        Source('QFlow/components/notify/icons/check.png', frozen=FROZEN_LIB).get(), 
        25, 25
    ),
    'error': lambda: Icon(
        Source('QFlow/components/notify/icons/close.png', frozen=FROZEN_LIB).get(), 
        25, 25
    ),
    'info': lambda: Icon(
        Source('QFlow/components/notify/icons/information.png', frozen=FROZEN_LIB).get(), 
    25, 25),
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