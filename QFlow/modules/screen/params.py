from dataclasses import dataclass
from qtpy.QtWidgets import QWidget

@dataclass
class ScreenParams:
    name: str = ''
    autoreloadUI: bool = False 
    autoUI: bool = True
    parentType: type  = None
    parent: QWidget = None