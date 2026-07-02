from .params import WindowParams
from copy import deepcopy
from dataclasses import asdict

def window(
    **kwargs
):
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
