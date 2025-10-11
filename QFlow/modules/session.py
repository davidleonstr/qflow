"""
This module defines a simple in-memory session storage class and a decorator to inject
this session storage into a class.

The `Session` class provides methods for storing, retrieving, and removing 
items from a session. The `session` decorator adds a `Session` 
attribute to a class, which allows easy access to the session storage.
"""

from ..core.temp import SESSION_STORAGE

def session():
    """
    A decorator that injects session storage into a class.

    This decorator adds a `Session` attribute to the class, making it 
    accessible from instances of the class.

    Returns:
        decorator: A class decorator that adds the `Session` attribute.
    """

    def decorator(cls):
        """
        Decorates a class to inject session storage.

        Args:
            cls: The class to decorate.

        Returns:
            cls: The decorated class with the `Session` attribute.
        """
        originalInit = cls.__init__

        def newInit(self, *args, **kwargs):
            """
            Initializes the decorated class and adds session storage.

            Args:
                *args: Positional arguments passed to the original class initializer.
                **kwargs: Keyword arguments passed to the original class initializer.
            """
            originalInit(self, *args, **kwargs)
            self.Session = SESSION_STORAGE

        cls.__init__ = newInit

        cls.Session = SESSION_STORAGE

        return cls
    
    return decorator