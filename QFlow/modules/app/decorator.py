from typing import Dict, Callable
from qtpy.QtGui import QIcon

def app(
    title: str,
    geometry: list[int],
    icon: Callable[[], QIcon],
    name: str = 'App',
    resizable: bool = True,
    maximizable: bool = True,
    strictClosingWindows: bool = True,
    opacity: float = 1.0,
    animatedEvents: Dict[str, bool] = None,
    animationValues: Dict[str, float] = None
):
    """
    Initializes the App with application-specific settings.

    Args:
        title (str): The title to set for the application window.
        geometry (list): The window geometry as a list [x, y, width, height].
        icon (Callable[[], QIcon]): Callable to make the icon to set for the window.
        name (str, optional): The name of the application window. Defaults to "App".
        resizable (bool, optional): Determines whether the window can be resized. Defaults to True.
        maximizable (bool, optional): Determines whether the window can be maximized. Defaults to True.
        strictClosingWindows (bool, optional): Determines whether all windows should be closed when the main window is closed. Defaults to True.
        opacity (float, optional): The opacity of the window. Defaults to 1.0.
        animatedEvents (Dict[str, bool], optional): Default animations for events.
        animationValues (Dict[str, float], optional): Default values for animations.
    """
    def decorator(cls):
        originit = getattr(cls, '__init__', None)

        def newinit(self, *args, **kwargs):
            super(cls, self).__init__(
                title=title,
                geometry=geometry if geometry is not None else [],
                icon=icon,
                name=name,
                resizable=resizable,
                maximizable=maximizable,
                strictClosingWindows=strictClosingWindows,
                opacity=opacity,
                animatedEvents=animatedEvents if animatedEvents is not None else {
                    'fadeIn': False, 'fadeOut': False
                },
                animationValues=animationValues if animationValues is not None else {
                    'opacityIncreasedIn': 0.02, 'opacityReductionOut': 0.02
                }
            )

            if originit:
                originit(self, *args, **kwargs)

        cls.__init__ = newinit
        return cls
    return decorator
