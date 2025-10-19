import sys
from pathlib import Path
import importlib.resources as res
import QFlow

class Source:
    """
    A helper class to resolve file paths correctly in both
    development mode and when the application is bundled with PyInstaller.

    This class automatically detects whether the code is running
    in a frozen (PyInstaller) environment or in a normal Python environment,
    and returns the correct absolute path to the requested resource.
    """

    def __init__(self, path: str):
        """
        Initialize a Source object.

        Args:
            path (str): The relative path of the resource inside the project/package.
        """
        self.frozen = QFlow.core.FROZEN_LIB
        self.basePath = sys._MEIPASS if self.frozen else str(res.files(QFlow))
        self.resolvedPath = str(Path(self.basePath, *Path(path).parts))

    def get(self) -> str:
        """
        Get the resolved absolute path of the resource.

        Returns:
            str: The absolute path to the requested resource.
        """
        return self.resolvedPath
