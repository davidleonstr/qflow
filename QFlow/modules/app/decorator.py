from copy import deepcopy
from dataclasses import asdict
from QFlow.modules.window import WindowParams

def app(
    **kwargs
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
    config = asdict(WindowParams(**kwargs))

    def decorator(cls):
        originit = getattr(cls, '__init__', None)

        def newinit(self, *args, **kwargs):
            super(cls, self).__init__(
                **config
            )

            self.args = deepcopy(config)

            if originit:
                originit(self, *args, **kwargs)

        cls.__init__ = newinit
        return cls

    return decorator
