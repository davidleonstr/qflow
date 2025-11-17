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
    
    All paths are resolved from the project root, just like normal Python behavior.
    """

    def __init__(self, path: str | Path, frozen: bool):
        """
        Initialize a Source object.

        Args:
            path (str | Path): The path of the resource from project root.
                Examples: "QFlow/resources/icon.png", "config/settings.yaml"
        """
        self.frozen = frozen
        self.inputPath = Path(path)
        
        # Check if it's an absolute path
        if self.inputPath.is_absolute():
            self.resolvedPath = str(self.inputPath)
        else:
            # Always resolve from project root
            if self.frozen:
                # In frozen mode, project root is sys._MEIPASS
                project_root = Path(sys._MEIPASS)
            else:
                # In dev mode, go up from QFlow package to project root
                package_path = Path(res.files(QFlow))
                project_root = package_path.parent
            
            self.resolvedPath = str(project_root / self.inputPath)

    def get(self) -> str:
        """
        Get the resolved absolute path of the resource.

        Returns:
            str: The absolute path to the requested resource.
        """
        return self.resolvedPath
    
    def exists(self) -> bool:
        """
        Check if the resolved path exists.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        return Path(self.resolvedPath).exists()
