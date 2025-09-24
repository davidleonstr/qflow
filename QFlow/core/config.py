from dataclasses import dataclass
import os

@dataclass
class QFlowDevConfiguration:
    USE_CONSOLE: bool = os.environ.get('QFLOW_USE_CONSOLE', True) in ['true', 'True', 'TRUE']