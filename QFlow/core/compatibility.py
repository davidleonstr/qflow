from .imports import (
    QTransformationMode, QWindowState, QWindowType, QAspectRatioMode,
    QWidgetAttribute, QAlignmentFlag, QCursorShape, QPenStyle, QEventType
)

class xQt:
    """Object intended for internal compatibility. Use at your own risk."""
    TransformationMode = QTransformationMode
    WindowState = QWindowState
    WindowType = QWindowType
    AspectRatioMode = QAspectRatioMode
    WidgetAttribute = QWidgetAttribute
    AlignmentFlag = QAlignmentFlag
    CursorShape = QCursorShape
    PenStyle = QPenStyle

class xQEvent:
    """Object intended for internal compatibility. Use at your own risk."""
    EventType = QEventType