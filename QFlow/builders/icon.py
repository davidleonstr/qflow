"""
This module defines the Icon class, which extends QPixmap to handle image loading and scaling.

The class ensures that an image is loaded only if the file exists. If the file does not exist, 
it initializes an empty QPixmap.
"""

import os
from qtpy.QtCore import Qt
from qtpy.QtGui import QPixmap

class Icon(QPixmap):
    """
    Planned for package use only.
    
    A QPixmap subclass that loads and scales an image if the file exists.

    This class checks whether the specified image file exists before loading it.
    If the file is found, it scales the image while maintaining its aspect ratio.
    Otherwise, it initializes an empty QPixmap.
    """

    def __init__(self, path: str, w: int, h: int):
        """
        Initializes an Icon object.

        Args:
            path (str): The file path of the image.
            w (int): The desired width of the icon.
            h (int): The desired height of the icon.
        """
        if os.path.exists(path):
            pixmap = QPixmap(path).scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            super().__init__(pixmap)
        else:
            super().__init__()