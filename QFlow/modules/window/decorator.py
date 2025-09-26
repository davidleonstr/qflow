from typing import Dict, Callable
from qtpy.QtGui import QIcon
from typing import Dict, Callable
from qtpy.QtGui import QIcon

def window(
    name: str = '',
    title: str = '',
    geometry: list[int] = None,
    maximizable: bool = True,
    icon: Callable[[], QIcon] = None,
    parentType=None,
    resizable: bool = True,
    strictClosingWindows: bool = True,
    opacity: float = 1.0,
    animatedEvents: Dict[str, bool] = None,
    animationValues: Dict[str, float] = None
):
    """
    Initializes the Window with specified properties and screen management.

    Args:
        name (str): The name of the window.
        title (str): The title of the window.
        geometry (list): The geometry of the window (ax: int, ay: int, aw: int, ah: int).
        maximizable (bool, optional): Determines whether the window can be maximized. Defaults to True.
        icon (Callable[[], QIcon]): Callable to make the icon to set for the window.
        parentType: Expected parent type for validation.
        resizable (bool, optional): The ability to resize the window. Defaults to True.
        strictClosingWindows (bool, optional): Determines whether all windows should be closed when the window is closed. Defaults to True.
        opacity (float, optional): The opacity of the window.
        animatedEvents (Dict[str, bool], optional): Default animations for events.
        animationValues (Dict[str, float], optional): Default values for animations.
    """
    def decorator(cls):
        originit = getattr(cls, '__init__', None)

        def newinit(self, *args, **kwargs):
            super(cls, self).__init__(
                name=name,
                title=title,
                geometry=geometry if geometry is not None else [],
                maximizable=maximizable,
                icon=icon,
                parent=None,
                parentType=parentType,
                resizable=resizable,
                strictClosingWindows=strictClosingWindows,
                opacity=opacity,
                animatedEvents=animatedEvents if animatedEvents is not None else {
                    'fadeIn': False, 'fadeOut': False
                },
                animationValues=animationValues if animationValues is not None else {
                    'opacityIncreasedIn': 0.02, 'opacityReductionOut': 0.02
                }
            )

            self.args = {
                'name': name,
                'title': title,
                'geometry': geometry if geometry is not None else [],
                'maximizable': maximizable,
                'icon': icon,
                'parentType': parentType,
                'resizable': resizable,
                'strictClosingWindows': strictClosingWindows,
                'opacity': opacity,
                'animatedEvents': animatedEvents if animatedEvents is not None else {
                    'fadeIn': False, 'fadeOut': False
                },
                'animationValues': animationValues if animationValues is not None else {
                    'opacityIncreasedIn': 0.02, 'opacityReductionOut': 0.02
                }
            }

            if originit:
                originit(self, *args, **kwargs)

        cls.__init__ = newinit
        return cls
    return decorator
