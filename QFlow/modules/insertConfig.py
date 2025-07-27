"""
This module defines a decorator for injecting a configuration object into a class.

The `insertConfig` decorator adds a `Config` attribute to a class, making the provided 
configuration available within the class. The configuration is passed during initialization 
and is accessible through the `Config` attribute.
"""

def insertConfig(config: object):
    """
    A decorator that injects a configuration object into a class.

    This decorator adds a `Config` attribute to the class, providing access to the 
    given configuration object.

    Args:
        config (object): The configuration object to be added to the class.

    Returns:
        decorator: A class decorator that adds the `Config` attribute.
    """

    def decorator(cls):
        """
        Decorates the class to add the configuration object as the `Config` attribute.

        Args:
            cls: The class to decorate.

        Returns:
            cls: The decorated class with the `Config` attribute.
        """
        originalInit = cls.__init__

        def newInit(self, *args, **kwargs):
            """
            Initializes the decorated class and adds the configuration.

            Args:
                *args: Positional arguments passed to the original class initializer.
                **kwargs: Keyword arguments passed to the original class initializer.
            """
            originalInit(self, *args, **kwargs)
            self.Config = config

        cls.__init__ = newInit

        cls.Config = config

        return cls
    
    return decorator