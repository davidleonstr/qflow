import sys

FROZENLIB = getattr(sys, 'frozen', False)
"""Flag to see if the package is frozen."""