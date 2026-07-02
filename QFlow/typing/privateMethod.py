import inspect
from functools import wraps

def privatemethod(func):
    'A decorator capable of enclosing a function within the context of the class that possesses it.'
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        frame = inspect.currentframe().f_back

        callerSelf = frame.f_locals.get('self')

        if callerSelf is not self:
            raise PermissionError(
                f"'{func.__name__}' is a private method."
            )

        return func(self, *args, **kwargs)

    return wrapper