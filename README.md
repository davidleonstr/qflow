<p align="center">
  <img src="assets/icons/QFlow-white-icon.svg" alt="Icon" width="200"/>
</p>

<p align="center">
  <img src="assets/icons/QFlow-white-text-icon.svg" alt="Text Icon" width="200"/>
</p>

# QFlow

**QFlow** is a Python microframework for building modern PyQt/PySide applications with a focus on simplicity and maintainability. It provides a comprehensive set of decorators and utilities that streamline the development of desktop interfaces by abstracting away common patterns and boilerplate code.

The microframework is designed to address the challenges of managing multiple windows, screens, and application state in PyQt/PySide applications. By leveraging decorators and a consistent architecture, QFlow enables developers to create applications with less code and better organization.

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
  - **Notifications**: Customizable notification.
  - **Floating Dialogs**: Modal dialog system.
  - **Toggle Switch**: Animated toggle switch component.

- **State Management**:
  - **Use State**: Reactive state management with getter, setter, and subscriber functions.
  - **Subscribeable**: Observable pattern implementation for global state management.
  - **Session Storage**: In-memory storage for temporary data between screens.
  - **Configuration**: Global configuration injection for application settings.

---

## Installation

> **Requirements:**
> - Python 3.11.3 or higher is required.
> - It is recommended to use a virtual environment (such as `venv`, `virtualenv`, or `conda`) to avoid dependency conflicts.
> - One of the following Qt frameworks: PyQt5, PyQt6, PySide2, or PySide6

### Qt Framework Compatibility

QFlow supports multiple Qt frameworks automatically. The framework is detected at runtime and the appropriate imports are used:

- **PyQt5**: `pip install PyQt5`
- **PyQt6**: `pip install PyQt6`
- **PySide2**: `pip install PySide2`
- **PySide6**: `pip install PySide6`

You only need to install one of these frameworks. QFlow will automatically detect and use the available framework.

#### Setting Qt Framework via Environment Variable

If you prefer to explicitly specify which Qt framework to use, you can set the `QFLOW_QT_FRAMEWORK` environment variable:

**Linux/macOS:**
```bash
export QFLOW_QT_FRAMEWORK=PySide6
python your_app.py
```

**Windows:**
```cmd
set QFLOW_QT_FRAMEWORK=PySide6
python your_app.py
```

**Python:**
```python
import os

os.environ['QFLOW_QT_FRAMEWORK'] = 'PySide6'

import QFlow
```

Valid values: `PyQt5`, `PyQt6`, `PySide2`, `PySide6`

```cmd
python -m venv venv
# On Linux use: source venv/bin/activate
./venv/Scripts/activate 
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
from QFlow.core import QIcon

@QFlow.mainWindow(
    title='Main Window', 
    geometry=[100, 100, 600, 400], 
    icon=lambda:QIcon(), 
    resizable=True, 
    maximizable=True
)
class MainWindowClass(QFlow.MainWindow):
    def __init__(self):
        super().__init__() # Necessary for initialization

        # Add screen
        screen = ScreenClass(self)
        self.cls.addScreen(screen)

        # Set the initial screen
        self.cls.setScreen(screen.name)
```

### Screen Definition

```python
import QFlow

@QFlow.screen(name='screen', autoreloadUI=False) 
class ScreenClass(QFlow.Screen):
    def __init__(
            self, 
            parent: QFlow.typing.MainWindowTyping # Or QFlow.typing.WindowTyping
        ): # Necessary for initialization
        super().__init__(parent) # Necessary for initialization
        self.screenParent = parent # Necessary if you want to be able to recharge your screen
        self.UI(parent) # Necessary if you want to be able to recharge your screen

    def UI(
            self, 
            parent: QFlow.typing.MainWindowTyping # Or QFlow.typing.WindowTyping
        ) -> None: # Necessary if you want to be able to recharge your screen
        """
        The entire UI is loaded here.
        """
        pass
```

### Window Definition

```python
import QFlow
from QFlow.core import QIcon

@QFlow.window(
    name='window', 
    title='Other Window', 
    geometry=[710, 100, 400, 150], 
    icon=lambda:QIcon(), 
    resizable=False
)
class WindowClass(QFlow.Window):
    def __init__(
            self, 
            parent: QFlow.typing.MainWindowTyping = None
        ): # When parent is None, it means it is an independent window
        super().__init__(parent) # Necessary for initialization
        self.mainWindow = parent # Necessary when it is a window dependent on the main window

        # Add screen
        screen = ScreenClass(self)
        self.cls.addScreen(screen)

        # Set the initial screen
        self.cls.setScreen(screen.name)
```

### Style Definition

```python
import QFlow
from QFlow.core import QWidget

# If style is a file path, use path = True
@QFlow.style(style='', path=True)
class AnyWidget(QWidget):
    pass
```

### Use Config Definition

```python
import QFlow
from QFlow.core import QWidget

config = object() # Any initialized object

@QFlow.useConfig(config)
class AnyClass:
    Config: object
```

### Use Session Storage Definition

```python
import QFlow

@QFlow.useSessionStorage()
class AnyClass:
    SessionStorage: QFlow.typing.SessionStorage # Object <SessionStorage>
```

</details>

## Definition of stores

<details>
<summary>Click to expand full stores definitions.</summary>

### Use Subscribeable Definition

```python
import QFlow

def printNewCounterValue(newValue):
    print(newValue)

counter = QFlow.stores.Subscribeable(0)
counter.subscribe(printNewCounterValue) 

def incrementCounter():
    counter.value = counter.value + 1

incrementCounter()

'''
If you want to unsubscribe from any feature:
counter.unsubscribe(printNewCounterValue)
'''
```

### Use State Definition

```python
import QFlow

def onCountChange(newValue):
    print(newValue)

count, setCount, subscribeCount, unSubscribeCount = QFlow.stores.useState(0)

subscribeCount(onCountChange)

def incrementCount():
    setCount(count() + 1)

incrementCount()

'''
If you want to unsubscribe from any feature:
unSubscribeCount(printNewCounterValue)
'''
```

</details>

## Definition of widgets

<details>
<summary>Click to expand full widgets definitions.</summary>

### Notify Definition

```python
import QFlow

# The notification appears as soon as the object is created.
QFlow.components.Notify(
    message='This is a notification!', 
    duration=3000, 
    parent=parent # Parent is necessarily a window object
)
```

### Dialog Definition

```python
import QFlow

dialog = QFlow.components.Dialog(
    parent=parent, # Parent is necessarily a window object
    childrenLayout=dialogLayout # A complete layout, if you have prepared it previously
)

closeDialogButton = QPushButton('Close Dialog')
closeDialogButton.clicked.connect(
    dialog.close # Function to close the dialog
)

# To add any widget to the dialog
dialog.addWidget(buttonDialog)

dialog.show() # Function to show the dialog
```

### Toggle Switch Definition

```python
import QFlow

toggle = QFlow.components.ToggleSwitch(
    parent=parent, # The parent of the element
    checked=True # Initial state
)

anyLayout.addWidget(toggle)
```

</details>

## How to run the examples

<details>
<summary>Click to expand instructions for running the examples in <code>examples/</code>.</summary>

You can find usage examples in the [`examples`](./examples) folder.

To run an example, use the following command in your terminal from the project root:

```bash
python examples/features_example.py
```

**Example descriptions:**
- <code>features_example.py</code>: Shows how to handle screens, windows, states, widgets, notifications, etc.

</details>

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