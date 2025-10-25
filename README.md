<p align="center">
  <img src="assets/icons/QFlow-white-icon.svg" alt="Icon" width="200"/>
</p>

<p align="center">
  <img src="assets/icons/QFlow-white-text-icon.svg" alt="Text Icon" width="200"/>
</p>

# QFlow

**QFlow** is a Python microframework for building modern PyQt/PySide applications with a focus on simplicity and maintainability. It provides a comprehensive set of decorators and utilities that streamline the development of desktop interfaces by abstracting away common patterns and boilerplate code.

**QFlow** is designed to address the challenges of managing multiple windows, screens, and application state in PyQt/PySide applications. By leveraging decorators and a consistent architecture, QFlow enables developers to create applications with less code and better organization.

---

## Installation

> **Requirements:**
> - Python 3.11.3 or higher is required.
> - It is recommended to use a virtual environment (such as `venv`, `virtualenv`, or `conda`) to avoid dependency conflicts.
> - One of the following Qt frameworks: pyqt5, pyqt6, pyside2, or pyside6

### Qt Framework Compatibility

QFlow supports multiple Qt frameworks automatically. The framework is detected at runtime and the appropriate imports are used:

- **PyQt5**: `pip install PyQt5`
- **PyQt6**: `pip install PyQt6`
- **PySide2**: `pip install PySide2`
- **PySide6**: `pip install PySide6`

You only need to install one of these frameworks. **QFlow** will automatically detect and use the available framework.

#### Setting Qt Framework via Environment Variable

If you prefer to explicitly specify which Qt framework to use, you can set the `QT_API` environment variable:

**Linux/macOS:**
```bash
export QT_API=pyside6
python app.py
```

**Windows:**
```cmd
set QT_API=pyside6
python app.py
```

**Python:**
```python
import os

os.environ['QT_API'] = 'pyside6'

import QFlow
```

Valid values: `pyqt5`, `pyqt6`, `pyside2`, `pyside6`

You can install **QFlow** directly from the source code by cloning the repository:

```bash
git clone https://github.com/davidleonstr/QFlow.git
cd QFlow
pip install .
```

Or using git + pip to install **QFlow** using the link to the repository:

```bash
pip install git+https://github.com/davidleonstr/QFlow.git
```

## Coding Style

<details>
<summary>QFlow follows the PyQt/PySide coding conventions and naming patterns.</summary>
<br>

- **Class Names**: Use PascalCase for class names.
- **Method Names**: Use camelCase for method names.
- **Variable Names**: Use camelCase for variable names.
- **Signal Names**: Use camelCase and start with a verb.
- **Slot Names**: Use camelCase and start with a verb.
- **Constants**: Use UPPER_CASE for constants.
- **Private Members**: Use underscore prefix for private members.

This consistent style makes the code more readable and maintainable, while following the established PyQt/PySide conventions.
</details>
