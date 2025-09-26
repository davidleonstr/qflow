import os

class GenericFile:
    def __init__(self, filepath) -> None:
        self.filepath: str = filepath
        self.readType: str = 'r'
        self.encoding: str = 'utf-8'
        self.writeType: str = 'w'

    def readFile(self, lines: bool=False) -> str | list | None:
        try:
            with open(file=self.filepath, mode=self.readType, encoding=self.encoding) as file:
                return file.read() if not lines else file.readlines()
        except FileNotFoundError:
            raise Exception(f"Error: File '{self.filepath}' does not exist.")
        except Exception as e:
            raise Exception(f'Unexpected error reading file: {e}')

    def writeFile(self, data: str) -> bool:
        try:
            with open(file=self.filepath, mode=self.writeType, encoding=self.encoding) as file:
                file.write(data)

            return True
        except PermissionError:
            raise Exception(f"Error: You do not have permissions to write to '{self.filepath}'.")
        except Exception as e:
            raise Exception(f'Unexpected error writing to file: {e}')

    def deleteFile(self) -> bool:
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
            return True
        
        return False