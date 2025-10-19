import sys

FROZEN_LIB = getattr(sys, 'frozen', False)

__all__ = ['FROZEN_LIB']