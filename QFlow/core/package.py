from rpack import ResourcePack
from ..utils import Source
from .flags import FROZEN_LIB

RESOURCE_PACKAGE_PATH = Source('QFlow/qflow.rpack', frozen=FROZEN_LIB).get()
"""Current package path with static files."""

RESOURCE_PACKAGE = ResourcePack(path=RESOURCE_PACKAGE_PATH)
"""Instance of the static resource package."""