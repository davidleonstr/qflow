from types import SimpleNamespace

class Object:
    """Class to create an object using a dictionary."""
    def __init__(self, data: dict):
        self.obj = self.toNamespace(data)

    def toNamespace(self, data):
        if isinstance(data, dict):
            return SimpleNamespace(**{k: self.toNamespace(v) for k, v in data.items()})
        elif isinstance(data, list):
            return [self.toNamespace(item) for item in data]
        else:
            return data