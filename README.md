<div align="center">
  <img src="assets/icons/QFlow-white-icon.svg" alt="QFlow Icon" width="180"/>
  <br/>
  <img src="assets/icons/QFlow-white-text-icon.svg" alt="QFlow Logo" width="220"/>
  
  <h3>A modern Python microframework for PyQt/PySide applications</h3>
  
  [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
  [![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

  [![PyQt5](https://img.shields.io/badge/PyQt5-supported-brightgreen.svg)](https://pypi.org/project/PyQt5/)
  [![PyQt6](https://img.shields.io/badge/PyQt6-supported-brightgreen.svg)](https://pypi.org/project/PyQt6/)
  [![PySide2](https://img.shields.io/badge/PySide2-supported-brightgreen.svg)](https://pypi.org/project/PySide2/)
  [![PySide6](https://img.shields.io/badge/PySide6-supported-brightgreen.svg)](https://pypi.org/project/PySide6/)
</div>

# QFlow

**QFlow** is a Python microframework for building modern PyQt/PySide applications with a focus on simplicity and maintainability. It provides a comprehensive set of decorators and utilities that streamline the development of desktop interfaces by abstracting away common patterns and boilerplate code.

## Installation

```bash
git clone https://github.com/davidleonstr/QFlow.git
cd QFlow
pip install .
```

```bash
pip install git+https://github.com/davidleonstr/QFlow.git
```

## Qt Framework Compatibility

QFlow supports multiple Qt frameworks automatically. The framework is detected at runtime and the appropriate imports are used:

- **PyQt5**: `pip install PyQt5`
- **PyQt6**: `pip install PyQt6`
- **PySide2**: `pip install PySide2`
- **PySide6**: `pip install PySide6`

If you prefer to explicitly specify which Qt framework to use, you can set the QT_API environment variable:

```python
import os

os.environ['QT_API'] = 'pyside6'

import QFlow
```
