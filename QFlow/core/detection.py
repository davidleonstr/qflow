import os

# List of frameworks and their versions
FLOW_PYQT_VERSIONS = ['PyQt5', 'PyQt6']
FLOW_PYSIDE_VERSIONS = ['PySide2', 'PySide6']
AVAILABLE_FRAMEWORKS = FLOW_PYQT_VERSIONS + FLOW_PYSIDE_VERSIONS

# Framework detection logic
_qt_framework = None
__framework__ = None

def _detect_framework():
    """Internal function to detect available Qt framework."""
    global _qt_framework, __framework__
    
    # Check for environment variable first
    env_framework = os.environ.get('QFLOW_QT_FRAMEWORK')
    if env_framework and env_framework in AVAILABLE_FRAMEWORKS:
        _qt_framework = env_framework
        __framework__ = __import__(env_framework)
        return
    
    # Auto-detection fallback
    for framework in AVAILABLE_FRAMEWORKS:
        try:
            __framework__ = __import__(framework)
            _qt_framework = framework
            return
        except ImportError:
            continue
    
    raise ImportError(f"No Qt framework found. Please install one of: {AVAILABLE_FRAMEWORKS}")

# Initialize framework detection
_detect_framework()

def getQtFramework() -> str:
    """Returns the detected Qt framework."""
    return _qt_framework

def isPyqt() -> bool:
    """Check if the current framework is PyQt."""
    return _qt_framework in FLOW_PYQT_VERSIONS

def isPyside() -> bool:
    """Check if the current framework is PySide."""
    return _qt_framework in FLOW_PYSIDE_VERSIONS

def getQtVersion() -> str:
    """Get the Qt version being used."""
    try:
        return __framework__.QtCore.PYQT_VERSION_STR if isPyqt() else __framework__.__version__
    except:
        return 'Unknown'

def getAvailableFrameworks() -> list[str]:
    """Get a list of available Qt frameworks in the current environment."""
    available = []
    for framework in AVAILABLE_FRAMEWORKS:
        try:
            __import__(framework)
            available.append(framework)
        except ImportError:
            pass
    return available