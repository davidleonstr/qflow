import json
import os
import re
from typing import Any, Dict, List
from QFlow.typing import privatemethod

class JSON:
    """
    Class to manage JSON files easily.
    Allows reading, writing, editing, and manipulating JSON files.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = None

    @privatemethod
    def resolve(self, data: Any, keys: list, create: bool = False) -> tuple[Any, str]:
        """
        Walk data following keys and return (parent, lastKey).

        Args:
            data:   Root object to traverse.
            keys:   List of key segments already split by '.'.
            create: If True, missing intermediate dicts are created.

        Returns:
            (parentNode, finalKey) so the caller can do parent[key].

        Raises:
            KeyError:  A segment does not exist and create=False.
            TypeError: A segment exists but its value is not a dict.
        """
        node = data
        for key in keys[:-1]:
            if isinstance(node, dict):
                if key not in node:
                    if create:
                        node[key] = {}
                    else:
                        raise KeyError(f"Key '{key}' not found.")
                node = node[key]
            else:
                raise TypeError(f"Expected a dict at '{key}', got {type(node).__name__}.")
        return node, keys[-1]

    def read(self) -> Dict[str, Any]:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return self.data
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{self.filepath}' does not exist.")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON: '{e}'", e.doc, e.pos)

    def write(self, data: Dict[str, Any], indent: int = 4) -> None:
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        self.data = data

    def create(self, data: Dict[str, Any] = None, indent: int = 4) -> None:
        self.write(data or {}, indent)

    def reload(self) -> Dict[str, Any]:
        return self.read()

    def exists(self) -> bool:
        return os.path.exists(self.filepath)
    
    def getAll(self) -> Dict[str, Any]:
        """
        Get all data.
        """
        if self.data is None:
            self.read()

        return self.data

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value using dot-notation key.
        """
        if self.data is None:
            self.read()
        try:
            parent, lastKey = self.resolve(self.data, key.split('.'))
            return parent.get(lastKey, default) if isinstance(parent, dict) else default
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """
        Set a value using dot-notation key, creating intermediate dicts when needed.
        """
        if self.data is None:
            self.read()
        parent, lastKey = self.resolve(self.data, key.split('.'), create=True)
        parent[lastKey] = value
        self.write(self.data)

    def delete(self, key: str) -> bool:
        """
        Delete a key using dot-notation. Returns True if deleted, False if not found.
        """
        if self.data is None:
            self.read()
        try:
            parent, lastKey = self.resolve(self.data, key.split('.'))
            if isinstance(parent, dict) and lastKey in parent:
                del parent[lastKey]
                self.write(self.data)
                return True
            return False
        except (KeyError, TypeError):
            return False

    def update(self, key: str, value: Any) -> None:
        """Update a top-level key (use set() for nested keys)."""
        if self.data is None:
            self.read()
        self.data[key] = value
        self.write(self.data)

    def merge(self, newData: Dict[str, Any]) -> None:
        if self.data is None:
            self.read()
        self.data.update(newData)
        self.write(self.data)

    def clear(self) -> None:
        self.data = {}
        self.write(self.data)

    def keys(self) -> List[str]:
        if self.data is None:
            self.read()
        return list(self.data.keys())

    def values(self) -> List[Any]:
        if self.data is None:
            self.read()
        return list(self.data.values())

    def items(self) -> List[tuple]:
        if self.data is None:
            self.read()
        return list(self.data.items())

    def indexar(self, data: Any = None, root: Dict[str, Any] = None) -> int:
        """
        Traverse all values in the JSON and replace '${key.key}/literal'
        references with their resolved value plus any surrounding literal text.

        Args:
            data: Current node (used internally for recursion).
            root: JSON root (used internally to resolve paths).

        Returns:
            Number of replacements made.

        Raises:
            ValueError: If a reference does not exist in the JSON or points
                        to a non-scalar value (dict or list).
        """
        PATTERN = re.compile(r'\$\{([^}]+)\}')

        if root is None:
            if self.data is None:
                self.read()
            root = self.data
            data = self.data

        def resolveRef(refKey: str) -> str:
            try:
                parent, lastKey = self.resolve(root, refKey.split('.'))
            except (KeyError, TypeError):
                raise ValueError(f"Reference '${{{refKey}}}' does not exist in the JSON.")
            if not isinstance(parent, dict) or lastKey not in parent:
                raise ValueError(f"Reference '${{{refKey}}}' does not exist in the JSON.")
            value = parent[lastKey]
            if isinstance(value, (dict, list)):
                raise ValueError(
                    f"Reference '${{{refKey}}}' points to an object/list, not a scalar value."
                )
            return str(value)

        def processNode(node: Any) -> tuple[Any, int]:
            count = 0

            if isinstance(node, dict):
                for key in node:
                    node[key], subCount = processNode(node[key])
                    count += subCount

            elif isinstance(node, list):
                for i, item in enumerate(node):
                    node[i], subCount = processNode(item)
                    count += subCount

            elif isinstance(node, str) and '${' in node:
                def replacer(match):
                    nonlocal count
                    count += 1
                    return resolveRef(match.group(1))
                node = PATTERN.sub(replacer, node)

            return node, count

        self.data, totalReplacements = processNode(data)
        return totalReplacements