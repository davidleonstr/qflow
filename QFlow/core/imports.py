from .detection import _qt_framework, __framework__

# Import the appropriate Qt modules based on the detected framework
if _qt_framework == "PyQt5":
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    
    pyqtProperty = pyqtProperty
    QEventType = QEvent
    QWindowState = Qt
    QWindowType = Qt
    QWidgetAttribute = Qt
    QAspectRatioMode = Qt
    QTransformationMode = Qt
    QAlignmentFlag = Qt
    QCursorShape = Qt
    QPenStyle = Qt

elif _qt_framework == "PySide2":
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    
    pyqtProperty = Property
    QEventType = QEvent
    QWindowState = Qt
    QWidgetAttribute = Qt
    QWindowType = Qt
    QAspectRatioMode = Qt
    QTransformationMode = Qt
    QAlignmentFlag = Qt
    QCursorShape = Qt
    QPenStyle = Qt

elif _qt_framework == "PySide6":
    from PySide6.QtWidgets import *
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    
    pyqtProperty = Property
    QEventType = QEvent.Type
    QWindowState = Qt.WindowState
    QWindowType = Qt.WindowType
    QWidgetAttribute = Qt.WidgetAttribute
    QAspectRatioMode = Qt.AspectRatioMode
    QTransformationMode = Qt.TransformationMode
    QAlignmentFlag = Qt.AlignmentFlag
    QCursorShape = Qt.CursorShape
    QPenStyle = Qt.PenStyle

elif _qt_framework == "PyQt6":
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    
    pyqtProperty = pyqtProperty
    QEventType = QEvent.Type
    QWindowState = Qt.WindowState
    QWindowType = Qt.WindowType
    QWidgetAttribute = Qt.WidgetAttribute
    QAspectRatioMode = Qt.AspectRatioMode
    QTransformationMode = Qt.TransformationMode
    QAlignmentFlag = Qt.AlignmentFlag
    QCursorShape = Qt.CursorShape
    QPenStyle = Qt.PenStyle