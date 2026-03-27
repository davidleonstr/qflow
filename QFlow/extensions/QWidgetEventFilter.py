"""
This module defines the QWidgetEventFilter class, which extends QObject to handle event filtering.

The class allows registering specific Qt events and associating them with callback functions.
When a registered event occurs on a widget, the corresponding callback is executed.
"""

from qtpy.QtCore import QObject

class QWidgetEventFilter(QObject):
    """
    Planned for package use only.

    A QObject subclass that provides a simple way to listen for Qt events on widgets.

    This class allows you to register event types and associate them with callback
    functions. When an event occurs, the corresponding function is executed with
    the widget as an argument.
    """

    def __init__(self):
        """
        Initializes a QWidgetEventFilter instance.

        Attributes:
            events (dict): A dictionary mapping event types (QEvent.Type)
                           to their associated callback functions.
        """
        super().__init__()
        self.events = {}

    def addEventToListen(self, event, action):
        """
        Registers an event and its associated callback function.

        Args:
            event (QEvent.Type): The Qt event type to listen for.
            action (callable): The function to execute when the event occurs.
                               The function must accept one argument (the widget).
        """
        self.events[event] = action

    def eventFilter(self, obj, event):
        """
        Intercepts events sent to the filtered object.

        Args:
            obj (QObject): The object receiving the event.
            event (QEvent): The event being processed.

        Returns:
            bool: Returns the base implementation result, allowing the event
                  to continue its normal processing.
        """
        for key, value in self.events.items():
            if event.type() == key:
                value(obj)

        return super().eventFilter(obj, event)