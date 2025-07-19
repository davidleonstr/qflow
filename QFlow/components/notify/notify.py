"""
This module defines the Notify class, which represents an on-screen notification in a PyQt5 application.

The class handles displaying messages with custom icons, progress bars, and predefined styles.
A decorator is used to apply styles from an external file.
"""

from ...core import QLabel, QVBoxLayout, QWidget, QProgressBar, QHBoxLayout, QFrame, QPixmap, QTimer, QWindowType, QWidgetAttribute, QAlignmentFlag
from typing import List, Dict

# Decorator for applying styles to PyQt5 widgets
from ...modules.style import *

# Class for creating Pixmap icons
from ...modules.icon import *

# Importing style properties and configuration
from .properties import STYLE_BAR, STYLE_PATH, STYLE_THEME_COLOR, ICONS

@style(STYLE_PATH, True)
class Notify(QWidget):
    """
    Represents an on-screen notification within a parent window.

    This class allows displaying messages with different notification types 
    (success, error, info) and customizable styles. It also includes a progress bar 
    indicating the notification duration.
    """

    cont = {}
    """Dictionary tracking the number of notifications per parent window."""

    def __init__(
            self, 
            message: str, 
            duration: int = 3000,
            delay: int = 0,
            parent=None, 
            type: str = 'success', 
            color: str = 'black', 
            customIcon: QPixmap = None,
            notificationsLimit: int = 7,
            characterLimit: int = 60,
            position: str = 'top-right',
            items: List[QWidget] = None,
            opacity: float = 1.0,
            animatedEvents: Dict[str, bool] = {},
            animationValues: Dict[str, float] = {},
            autoShow: bool = True
        ):
        """
        Initializes a Notify object.

        Args:
            message (str): The notification message.
            duration (int, optional): Duration before the notification disappears (in milliseconds). Default is 3000ms.
            delay (int, optional): Delay before showing the notification (in milliseconds). Default is 0ms.
            parent (QWidget, optional): The parent widget where the notification will be displayed. It's usually the window.
            type (str, optional): The type of notification ('success', 'error', 'info'). Default is 'success'.
            color (str, optional): The theme color ('black' or 'white'). Default is 'black'.
            customIcon (QPixmap, optional): A custom icon to use instead of the default.
            notificationsLimit (int, optional): Parent notification limiter. Default is 7.
            characterLimit (int, optional): Character limit in the notification. Default is 60.
            position (str, optional): Position of the notification ('top-right', 'top-left', 'bottom-right', 'bottom-left'). Default is 'top-right'.
            items (List[QWidget], optional): Widgets to add to the notification. Default is None.
            opacity: (float, optional): The opacity of the notify.
            animatedEvents: (Dict[str, bool], optional): Default animations for events to {'fadeIn': True, 'fadeOut': True}.
            animationValues: (Dict[str, bool], optional): Default values for animations {'opacityIncreasedIn': 0.05, 'opacityReductionOut': 0.05}.
            autoShow: (bool, optional): Whether to show the notification automatically after creation. Default is True.
        """
        super().__init__(parent)
        self.parent = parent
        self.duration = duration
        self.delay = delay
        self.elapsedTime = 0
        self.message = message
        self.position = position
        self.items = items
        self.opacity = opacity
        self.msRenderTime = 16
        self.isVisible = False
        self.isShown = False
        self.autoShow = autoShow
        self.notificationsLimit = notificationsLimit

        self._animationValues = {
            'opacityIncreasedIn': 0.05,
            'opacityReductionOut': 0.05
        } 
        self._animationValues.update(animationValues)

        self._animatedEvents = {
            'fadeIn': True,
            'fadeOut': True
        }
        self._animatedEvents.update(animatedEvents)

        if len(message) > characterLimit:
            self.message = message[:characterLimit - 1] + '...'

        self.setWindowFlags(QWindowType.FramelessWindowHint | QWindowType.Tool)
        self.setAttribute(QWidgetAttribute.WA_TranslucentBackground)

        self.container = QFrame(self)
        self.container.setMinimumWidth(270)
        self.container.setMaximumWidth(self.parent.width())

        if color in STYLE_THEME_COLOR:
            self.containerStyle = STYLE_THEME_COLOR[color]['QFrame']
        else:
            raise KeyError(f"The color does not exist in Notify: '{color}'")

        self.container.setObjectName(self.containerStyle)

        self.iconLabel = QLabel(self.container)

        if type in ICONS:
            self.icon = ICONS[type]()

        if customIcon is not None:
            self.icon = customIcon

        self.iconLabel.setPixmap(self.icon)

        self.messageLabel = QLabel(self.message, self.container)

        if color in STYLE_THEME_COLOR:
            self.messageLabel.setObjectName(STYLE_THEME_COLOR[color]['QLabel'])
        else:
            raise KeyError(f"The color does not exist in Notify: '{color}'")

        self.progressBar = QProgressBar(self.container)

        if type in STYLE_BAR:
            self.progressBarStyle = STYLE_BAR[type]
        else:
            raise KeyError(f"The type does not exist in Notify: '{type}'")

        self.progressBar.setObjectName(self.progressBarStyle)

        self.progressBar.setFixedHeight(10)
        self.progressBar.setTextVisible(False)
        self.progressBar.setMaximum(self.duration)
        self.progressBar.setValue(0)

        self.contentLayout = QHBoxLayout()
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setSpacing(8)
        self.contentLayout.addWidget(self.iconLabel, 0, QAlignmentFlag.AlignVCenter)  
        self.contentLayout.addWidget(self.messageLabel, 1, QAlignmentFlag.AlignVCenter)

        self.containerLayout = QVBoxLayout(self.container)
        self.containerLayout.addLayout(self.contentLayout)
        self.containerLayout.addWidget(self.progressBar)

        if self.items is not None:
            for widget in items:
                if isinstance(widget, QWidget):
                    self.containerLayout.addWidget(widget)

        self.containerLayout.setContentsMargins(20, 10, 20, 10)

        self.container.setLayout(self.containerLayout)
        self.container.adjustSize()

        # Check notification limit before incrementing counter
        if self.parent in Notify.cont:
            if Notify.cont[self.parent] >= notificationsLimit:
                self.limitExceeded = True
                return  # Don't create notification if limit exceeded
        else:
            Notify.cont[self.parent] = 0
        
        self.limitExceeded = False

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.container)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)
        self.adjustSize()

        # Initialize timers but don't start them yet
        self.positionTimer = QTimer(self)
        self.positionTimer.timeout.connect(self.updatePosition)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgress)

        # Handle auto-show behavior
        if self.autoShow:
            self.show()

    def show(self) -> None:
        """Shows the notification. Can be called manually to control when the notification appears."""
        if self.isShown or self.limitExceeded:
            return  # Don't show if already shown or limit exceeded
        
        self.isShown = True
        
        # Handle delay
        if self.delay > 0:
            # Schedule the notification to show after delay
            QTimer.singleShot(self.delay, self._showNotification)
        else:
            # Show immediately if no delay
            self._showNotification()

    def _showNotification(self) -> None:
        """Shows the notification after the delay period."""
        # Increment counter only when actually showing
        Notify.cont[self.parent] += 1
        self.notificationCount = Notify.cont[self.parent]
        
        self.updatePosition()
        
        # Start timers
        self.positionTimer.start(self.msRenderTime)  # Approximately 60 fps
        self.timer.start(self.msRenderTime)  # Approximately 60 fps
        
        # Schedule auto-close
        QTimer.singleShot(self.duration, self.close)
        
        # Set opacity
        if self.opacity != 1.0:
            self.setWindowOpacity(self.opacity)
        
        # Handle fade-in animation
        if self._animatedEvents['fadeIn']:
            self._animateFadeIn()
        
        # Mark as visible and show
        self.isVisible = True
        super().show()  # Call the parent's show method

    def _animateFadeOut(self) -> None:
        timer = QTimer(self)
        opacity = self.windowOpacity()

        def _modifyOpacity():
            nonlocal opacity
            opacity -= self._animationValues['opacityReductionOut']

            if opacity <= 0.1:
                timer.stop()
                    
            self.setWindowOpacity(opacity)

        timer.timeout.connect(_modifyOpacity)
        timer.start(self.msRenderTime)

    def _animateFadeIn(self) -> None:
        self.setWindowOpacity(0.1)
        timer = QTimer(self)
        opacity = self.windowOpacity()

        def _modifyOpacity():
            nonlocal opacity
            opacity += self._animationValues['opacityIncreasedIn']

            if opacity >= self.opacity:
                timer.stop()
                    
            self.setWindowOpacity(opacity)

        timer.timeout.connect(_modifyOpacity)
        timer.start(self.msRenderTime)

    def updatePosition(self) -> None:
        """Updates the notification's position relative to its parent window based on the specified position."""
        if self.parent:
            if not self.parent.isVisible():
                self.close()
                
            margin = 20
            betweenMargin = 20
            notificationHeight = self.height() + betweenMargin
            
            if 'right' in self.position:
                x = self.parent.x() + self.parent.width() - self.width() - margin
            else:
                x = self.parent.x() + margin
            
            if 'top' in self.position:
                y = self.parent.y() + 40 + (self.notificationCount - 1) * notificationHeight
            else:
                y = (self.parent.y() + self.parent.height() - self.notificationCount * notificationHeight)
            
            self.move(x, y)

    def updateProgress(self) -> None:
        """Updates the progress bar and closes the notification when the duration ends."""
        self.elapsedTime += 30
        self.progressBar.setValue(self.elapsedTime)

        if self.elapsedTime >= self.duration:
            self.timer.stop()
            if self._animatedEvents['fadeOut']:
                self._animateFadeOut()
                QTimer.singleShot(200, self.close)
            else:
                self.close()

    def hide(self) -> None:
        """Hides the notification without closing it."""
        if self.isVisible:
            super().hide()
            self.isVisible = False
            if self.positionTimer.isActive():
                self.positionTimer.stop()
            if self.timer.isActive():
                self.timer.stop()

    def isNotificationVisible(self) -> bool:
        """Returns True if the notification is currently visible."""
        return self.isVisible

    def isNotificationShown(self) -> bool:
        """Returns True if show() has been called on this notification."""
        return self.isShown

    def close(self) -> None:
        """Closes the notification and updates the notification count."""
        if self.isVisible and self.parent in Notify.cont and Notify.cont[self.parent] > 0:
            Notify.cont[self.parent] -= 1
        super().close()