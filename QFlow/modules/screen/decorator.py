def screen(name: str, autoreloadUI: bool = False, autoUI: bool = True, parentType = None):
    """
    Initialize the Screen object.
        
    Args:
        name (str): The name to assign to the screen.
        autoreloadUI (bool): If True, ensures the class has a `UI` method and reloads it on show.
        autoUI (bool): Executes the UI function during the showEvent without having to call it.
        parentType: Expected parent type for validation.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.
    """
    def decorator(cls):
        originit = getattr(cls, '__init__', None)

        def newinit(self, *args, **kwargs):
            super(cls, self).__init__(
                name=name,
                autoreloadUI=autoreloadUI,
                autoUI=autoUI,
                parentType=parentType
            )

            self.args = {
                'name': name,
                'autoreloadUI': autoreloadUI,
                'autoUI': autoUI,
                'parentType': parentType
            }

            if originit:
                originit(self, *args, **kwargs)

        cls.__init__ = newinit
        return cls
    return decorator
