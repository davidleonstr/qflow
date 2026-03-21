from qtpy.QtGui import QIcon

def window(
    name: str = '',
    title: str = '',
    geometry: list[int] = None,
    maximizable: bool = True,
    icon: QIcon = None,
    parentType=None,
    resizable: bool = True,
    strictClosingWindows: bool = True,
    opacity: float = 1.0,
    frameless: bool = False
):
    """
    Initializes the Window with specified properties and screen management.

    Args:
        name (str): The name of the window.
        title (str): The title of the window.
        geometry (list): The geometry of the window (ax: int, ay: int, aw: int, ah: int).
        maximizable (bool, optional): Determines whether the window can be maximized. Defaults to True.
        icon (QIcon): The icon to set for the window.
        parentType: Expected parent type for validation.
        resizable (bool, optional): The ability to resize the window. Defaults to True.
        strictClosingWindows (bool, optional): Determines whether all windows should be closed when the window is closed. Defaults to True.
        opacity (float, optional): The opacity of the window.
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
                frameless=frameless
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
                'frameless': frameless
            }

            if originit:
                originit(self, *args, **kwargs)

        cls.__init__ = newinit
        return cls
    return decorator
