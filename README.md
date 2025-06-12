# QFlow

**QFlow** is a Python microframework for building modern PyQt5 applications with a focus on simplicity and maintainability. It provides a comprehensive set of decorators and utilities that streamline the development of desktop interfaces by abstracting away common patterns and boilerplate code.

The microframework is designed to address the challenges of managing multiple windows, screens, and application state in PyQt5 applications. By leveraging decorators and a consistent architecture, QFlow enables developers to create applications with less code and better organization.

---

## Key Features

- **Window Management**:
  - Create and manage multiple windows with the `@window` decorator.
  - Build main application windows with the `@mainWindow` decorator.
  - Navigate between windows with history tracking.
  - Customize window properties.

- **Screen Management**:
  - Create and navigate between multiple screens with the `@screen` decorator.
  - Automatic screen transitions with history tracking.
  - Support for screen-specific layouts and widgets.
  - Optional automatic UI reload when screens are displayed.

- **Style Management**:
  - Apply styles to windows and widgets using the `@style` decorator.
  - Support for both file-based and string-based stylesheets.
  - Theme color customization for consistent UI.

- **Configuration Management**:
  - Inject global configurations with the `@useConfig` decorator.
  - Access application settings from any component.
  - Centralized configuration management.

- **Session Storage**:
  - In-memory session storage with the `@useSessionStorage` decorator.
  - Store and retrieve temporary data between screens.
  - Persistent data management during application runtime.

- **UI Components**:
  - **Notifications**: Customizable notification system with different types (success, error, info) and progress bars.
  - **Floating Dialogs**: Modal dialog system with customizable backdrop, supporting both white and black themes.
  - **Toggle Switch**: Animated toggle switch component with customizable appearance.

- **State Management**:
  - **Use State**: React-like state management with getter, setter, and subscriber functions.
  - **Subscribeable**: Observable pattern implementation for global state management.
  - **Session Storage**: In-memory storage for temporary data between screens.
  - **Configuration**: Global configuration injection for application settings.

---

## Installation

> **Requirements:**
> - Python 3.11.3 or higher is required.
> - It is recommended to use a virtual environment (such as `venv`, `virtualenv`, or `conda`) to avoid dependency conflicts.

```bash
# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

You can install **QFlow** directly from the source code by cloning the repository:

```bash
git clone https://github.com/davidleonstr/QFlow.git
cd QFlow
pip install .
```

Or using git + pip to install **QFlow** using the link to the repository:

```bash
pip install git+clone https://github.com/davidleonstr/QFlow.git
```

**For development:**
```bash
git clone https://github.com/davidleonstr/QFlow.git
cd QFlow
pip install -e .
```

## Definition of decorators

<details>
<summary>Click to expand full decorator definitions.</summary>

### Main Window Definition

```python
import QFlow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget
from typing import Callable, Dict, List

@QFlow.mainWindow(
    title='Main Window', 
    geometry=[100, 100, 600, 400], 
    icon=QIcon(), 
    resizable=True, 
    maximizable=True
)
class MainWindowClass(QMainWindow):
    # Type hints for better IDE support
    title: str
    windowGeometry: List
    icon: QIcon
    screenHistory: List[str]
    stackedScreens: QStackedWidget
    addScreen: Callable[[QWidget], None]
    setScreen: Callable[[str], None]
    createWindow: Callable[[QMainWindow], None]
    setWindow: Callable[[str], None]
    closeWindow: Callable[[str], None]
    onWindowClose: Callable[[], None]
    removeWindow: Callable[[str], None]
    goBack: Callable[[], None]
    screens: Dict[str, QWidget]
    windows: Dict[str, QMainWindow]

    def __init__(self):
        super().__init__() # Necessary for initialization

        # Add screen
        screen = ScreenClass(self)
        self.addScreen(screen)

        # Set the initial screen
        self.setScreen(screen.name)
```

### Screen Definition

```python
import QFlow
from PyQt5.QtWidgets import QWidget
from typing import Callable

@QFlow.screen(name='screen', autoreloadUI=False) 
class ScreenClass(QWidget):
    # Type hints for better IDE support
    name: str
    screenName: str
    reloadUI: Callable[[], None]
    setScreenName: Callable[[str], None]
    removeAllLayouts: Callable[[], None]

    def __init__(self, parent): # Necessary for initialization
        super().__init__(parent) # Necessary for initialization
        self.widgetParent = parent # Necessary if you want to be able to recharge your screen
        self.UI(parent) # Necessary if you want to be able to recharge your screen

    def UI(self, parent) -> None: # Necessary if you want to be able to recharge your screen
        """
        The entire UI is loaded here.
        """
        pass
```

### Window Definition

```python
import QFlow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget
from typing import Callable, List, Dict

@QFlow.window(
    name='window', 
    title='Other Window', 
    geometry=[710, 100, 400, 150], 
    icon=QIcon(), 
    resizable=False
)
class WindowClass(QMainWindow):
    # Type hints for better IDE support
    title: str
    name: str
    windowGeometry: List
    icon: QIcon
    screenHistory: List[str]
    stackedScreens: QStackedWidget
    addScreen: Callable[[QWidget], None]
    setScreen: Callable[[str], None]
    setWindowName: Callable[[str], None]
    goBack: Callable[[], None]
    screens: Dict[str, QWidget]

    def __init__(self, parent=None): # When parent is None, it means it is an independent window
        super().__init__(parent) # Necessary for initialization
        self.mainWindow = parent # Necessary when it is a window dependent on the main window

        # Add screen
        screen = ScreenClass(self)
        self.addScreen(screen)

        # Set the initial screen
        self.setScreen(screen.name)
```

### Style Definition

```python
import QFlow
from PyQt5.QtWidgets import QWidget

# If style is a file path, use path = True
@QFlow.style(style='', path=True)
class AnyWidget(QWidget):
    pass
```

### Use Config Definition

```python
import QFlow
from PyQt5.QtWidgets import QWidget

config = object() # Any initialized object

@QFlow.useConfig(config)
class AnyClass:
    Config: object
```

### Use Session Storage Definition

```python
import QFlow
from PyQt5.QtWidgets import QWidget
from typing import Callable, Any

class SessionStorage:
    setItem: Callable[[str, Any], None]
    getItem: Callable[[str], Any]
    removeItem: Callable[[str], Any]

@QFlow.useSessionStorage()
class AnyClass:
    SessionStorage: SessionStorage # Object <SessionStorage>
```

</details>

## How to run the examples

<details>
<summary>Click to expand instructions for running the examples in <code>examples/</code>.</summary>

You can find usage examples in the [`examples`](./examples) folder.

To run an example, use the following command in your terminal from the project root:

```bash
python examples/feature_sample.py
```

**Example descriptions:**
- <code>feature_sample.py</code>: Shows how to handle screens, windows, states, widgets, notifications, etc.

</details>

## Coding Style

<details>
<summary>QFlow follows the PyQt5 coding conventions and naming patterns.</summary>
<br>

- **Class Names**: Use PascalCase for class names.
- **Method Names**: Use camelCase for method names.
- **Variable Names**: Use camelCase for variable names.
- **Signal Names**: Use camelCase and start with a verb.
- **Slot Names**: Use camelCase and start with a verb.
- **Constants**: Use UPPER_CASE for constants.
- **Private Members**: Use underscore prefix for private members.

This consistent style makes the code more readable and maintainable, while following the established PyQt5 conventions.
</details>