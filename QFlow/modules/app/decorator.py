from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QIcon
from typing import Callable

def app(
    title: str,
    geometry: list[int],
    icon: Callable[[], QIcon] = None,
    name: str = 'App',
    customTemplate: Callable[[], QWidget] = None,
    resizable: bool = True,
    maximizable: bool = True,
    strictClosingWindows: bool = True,
    opacity: float = 1.0,
    frameless: bool = False
):
    """
    Initializes the App with application-specific settings.

    Args:
        title (str): The title to set for the application window.
        geometry (list): The window geometry as a list [x, y, width, height].
        icon (QIcon): Callable of the icon to set for the window.
        name (str, optional): The name of the application window. Defaults to "App".
        customTemplate (QWidget): Callable of custom QWidget as a template. It needs to have a QStackedWidgets named 'screens' in order to render the screens there.
        resizable (bool, optional): Determines whether the window can be resized. Defaults to True.
        maximizable (bool, optional): Determines whether the window can be maximized. Defaults to True.
        strictClosingWindows (bool, optional): Determines whether all windows should be closed when the main window is closed. Defaults to True.
        opacity (float, optional): The opacity of the window. Defaults to 1.0.
        frameless (bool, optional): It can delete the window frame.
    """
    def decorator(cls):
        originit = getattr(cls, '__init__', None)

        def newinit(self, *args, **kwargs):
            super(cls, self).__init__(
                title=title,
                geometry=geometry if geometry is not None else [],
                icon=icon,
                customTemplate=customTemplate,
                name=name,
                resizable=resizable,
                maximizable=maximizable,
                strictClosingWindows=strictClosingWindows,
                opacity=opacity,
                frameless=frameless
            )

            if originit:
                originit(self, *args, **kwargs)

        cls.__init__ = newinit
        return cls
    return decorator
