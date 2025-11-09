import sys

FROZEN_LIB = getattr(sys, 'frozen', False)
"""Flag to see if the package is frozen."""