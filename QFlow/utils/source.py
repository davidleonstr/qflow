import sys
from pathlib import Path
import importlib.resources as res
import QFlow
from QFlow.core import FROZENLIB

class Source:
    def __init__(
        self,
        path: str | Path,
        root: Path
    ):
        self.inputPath = Path(path)

        if self.inputPath.is_absolute():
            self.resolvedPath = self.inputPath
        else:
            self.resolvedPath = (root / self.inputPath).resolve()

    @classmethod
    def library(cls, path: str | Path) -> "Source":
        """
        Resolve a path relative to the QFlow package.
        """

        if FROZENLIB:
            root = Path(sys._MEIPASS)
        else:
            root = Path(res.files(QFlow)).resolve().parent

        return cls(path, root)

    @classmethod
    def project(cls, path: str | Path) -> "Source":
        """
        Resolve a path relative to the user's project.
        """

        if FROZENLIB:
            root = Path(sys.executable).parent
        else:
            root = Path.cwd()

        return cls(path, root)

    def get(self) -> str:
        """
        Get the resolved path.
        """
        return str(self.resolvedPath)

    def exists(self) -> bool:
        """
        Check if the path exists.
        """
        return self.resolvedPath.exists()

    def path(self) -> Path:
        """
        Get the resolved Path object.
        """
        return self.resolvedPath

    def __str__(self) -> str:
        return str(self.resolvedPath)

    def __fspath__(self):
        return str(self.resolvedPath)