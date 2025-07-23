"""
This module defines the ToggleSwitch class, a customizable animated toggle switch widget for PyQt5.

The class provides a clickable switch that toggles between ON and OFF states with smooth animations.
It supports color customization and state querying.
"""

from qtpy.QtCore import Qt, QPropertyAnimation, Property
from qtpy.QtGui import QColor, QPainter, QBrush, QCursor
from qtpy.QtWidgets import QWidget

class ToggleSwitch(QWidget):
    """
    Represents a custom animated toggle switch.

    This widget mimics a modern switch with animation and customizable colors.
    The circle smoothly slides between ON and OFF states upon click, and
    emits visual feedback based on the internal boolean state.
    """

    def __init__(
            self, 
            parent, 
            width: int = 50, 
            height: int = 25,
            # num ≠ 0 ⇔ True: It's the same as on or off
            bgColor: list[str] = ['#ccc', '#00c853'],
            circleColor: str = '#fff',
            checked: bool = False
        ):
        """
        Initializes the ToggleSwitch object.

        Args:
            parent (QWidget): The parent widget.
            width (int, optional): The width of the toggle. Default is 50.
            height (int, optional): The height of the toggle. Default is 25.
            bgColor (list, optional): List of two colors [offColor, onColor] in hex format.
            circleColor (str, optional): Color of the sliding circle in hex format.
        """
        super().__init__(parent)
        self.setFixedSize(width, height)
        self._checked = False
        self._circlePosition = 2

        self._animation = QPropertyAnimation(self, b"circlePosition")
        self._animation.setDuration(150)

        self._bgColorOn = QColor(bgColor[1])
        self._bgColorOff = QColor(bgColor[0])
        self._circleColor = QColor(circleColor)

        self.setChecked(checked)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def mousePressEvent(self, event):
        """
        Handles the mouse press event to toggle the switch state.

        Args:
            event (QMouseEvent): The mouse event.
        """
        self._checked = not self._checked
        self._animate()
        self.update()
        super().mousePressEvent(event)

    def _animate(self):
        """
        Performs the circle sliding animation based on the current state.
        """
        start = self._circlePosition
        end = self.width() - self.height() + 2 if self._checked else 2
        self._animation.stop()
        self._animation.setStartValue(start)
        self._animation.setEndValue(end)
        self._animation.start()

    def paintEvent(self, event):
        """
        Paints the switch background and sliding circle.

        Args:
            event (QPaintEvent): The paint event.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg_color = self._bgColorOn if self._checked else self._bgColorOff
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)

        painter.setBrush(QBrush(self._circleColor))
        painter.drawEllipse(self._circlePosition, 2, self.height() - 4, self.height() - 4)

    def isChecked(self):
        """
        Returns:
            bool: The current checked state of the switch.
        """
        return self._checked

    def setChecked(self, checked: bool):
        """
        Sets the checked state of the switch and updates its position immediately.

        Args:
            checked (bool): The desired checked state.
        """
        self._checked = checked
        self._animate()
        self.update()

    def getCirclePosition(self):
        """
        Returns:
            int: The current X position of the circle.
        """
        return self._circlePosition

    def setCirclePosition(self, pos):
        """
        Updates the X position of the circle (used by the animation).

        Args:
            pos (int): The new position.
        """
        self._circlePosition = pos
        self.update()

    circlePosition = Property(int, fget=getCirclePosition, fset=setCirclePosition)