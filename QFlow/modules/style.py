"""
This module defines a decorator for applying stylesheets to PyQt5 widgets or windows.

The `style` decorator is used to apply a style to a widget or window either from a file path 
or directly as a string. It modifies the `__init__` method of the decorated class to include 
the stylesheet application.
"""

from ..utils.genericFile import GenericFile

def style(style: str, path: bool = False):
    """
    A decorator that applies a stylesheet to a widget or window.

    This decorator either applies a style from a file path or directly as a string to 
    the widget or window that the decorator is applied to. If `path` is set to `True`, 
    the `style` is treated as a file path, and the stylesheet is read from the file. 
    Otherwise, the `style` is applied directly as a string.

    Args:
        style (str): The stylesheet or the path to the stylesheet file.
        path (bool): Whether the `style` argument is a file path. Defaults to `False`.

    Returns:
        decorator: A class decorator that applies the given style to the widget/window.
    """

    def decorator(cls):
        """
        Decorates the class to apply the given stylesheet.

        Args:
            cls: The class to decorate.

        Returns:
            cls: The decorated class with the stylesheet applied.
        """
        originalInit = cls.__init__

        def newInit(self, *args, **kwargs):
            """
            Initializes the decorated class and applies the stylesheet.

            Args:
                *args: Positional arguments passed to the original class initializer.
                **kwargs: Keyword arguments passed to the original class initializer.
            """
            originalInit(self, *args, **kwargs)

            if path:
                styleSheet = GenericFile(style).readFile()

            try:
                self.setStyleSheet(styleSheet if path else style)
            except:
                raise TypeError(f'{self} is not a stylizable object')

        cls.__init__ = newInit

        return cls
    
    return decorator