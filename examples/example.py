import os
import sys

# For debug
import json

os.environ['QT_API'] = 'pyqt6'
# The library that will be used internally is assigned.

from qtpy.QtWidgets import (
    QApplication, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit
)
from qtpy.QtGui import QIcon

import QFlow
# The package is imported

from QFlow.components import Notify
# The notification class is imported from QFlow components

@QFlow.app(
    title='QFlow App Title', 
    geometry=[100, 100, 800, 600], 
    icon=lambda: QIcon(),
    animatedEvents={
        'fadeIn': True,
        'fadeOut': True
    }
)
# The class is initialized with predefined arguments using the decorator corresponding to the class
class QFlowApp(QFlow.App):
    def __init__(self):
        # Definition of window
        self.secondaryWindow = QFlowSecondaryWindow()

        # Definition of screens
        self.mainScreen = QFlowMainScreen(parent=self)
        self.secondMovementScreen = QFlowSecondMovementScreen(parent=self)

        # Adding screens
        self.addScreen(screen=self.mainScreen)
        self.addScreen(screen=self.secondMovementScreen)

        # The main screen is set with parameters
        self.setScreen(name=self.mainScreen.name, args={
            'from': self.name,
            'to': self.mainScreen.name
        })

        # Creation of window with parameters
        self.createWindow(self.secondaryWindow, args={
            'from': self.name,
            'to': self.secondaryWindow.name
        })

        # A notification is created
        Notify(message='Hello', parent=self)

@QFlow.window(
    name='secondaryWindow',
    title='QFlow Secondary Window',
    geometry=[150, 150, 400, 300], 
    icon=lambda: QIcon(),
    animatedEvents={
        'fadeIn': True,
        'fadeOut': True
    }
)
# The class is initialized with predefined arguments using the decorator corresponding to the class
class QFlowSecondaryWindow(QFlow.Window):
    def __init__(self):
        # Definition of screen
        self.secondaryScreen = QFlowSecondaryScreen(self)

        # Adding screen
        self.addScreen(screen=self.secondaryScreen)

        # The main screen is set
        self.setScreen(name=self.secondaryScreen.name)
    
    def effect(self):
        """
        It runs whenever the screen is created or set.
        """
        # The parameters that were previously passed to the object are obtained
        self.params = QFlow.hooks.Params(self)

        # For debug
        print(json.dumps(self.params.get(), indent=4))

@QFlow.screen(
    name='mainScreen',
    autoreloadUI=True,
    parentType=QFlow.App
)
# The class is initialized with predefined arguments using the decorator corresponding to the class
class QFlowMainScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        """
        The 'parent' argument is added to the predefined arguments using the 
        'args' property on each object using the 'screen' decorator.
        """
        # The arguments are passed to super init
        super().__init__(**self.args)

    def effect(self):
        """
        It runs whenever the screen is created or set.
        """
        # The parameters that were previously passed to the object are obtained
        self.params = QFlow.hooks.Params(self)

        # For debug
        print(json.dumps(self.params.get(), indent=4))
    
    def UI(self):
        """
        Function where the entire screen UI is executed and must be initialized
        """
        self.label = QLabel('Hello!')
        self.nameLabel = QLabel(f'Screen: {self.name}')

        self.screenSelectionInput = QLineEdit()
        self.screenSelectionInput.setPlaceholderText('Screen Name')

        self.moveToButton = QPushButton('Move to')

        # The parent (window || app) is obtained and a screen is set
        self.moveToButton.clicked.connect(
            lambda: self.parent()
            .setScreen(
                name=self.screenSelectionInput
                .text()
                .strip()
            )
        )

        self.screenSelectionLayout = QHBoxLayout()
        self.screenSelectionLayout.addWidget(self.moveToButton)
        self.screenSelectionLayout.addWidget(self.screenSelectionInput)

        self.reloadButton = QPushButton('Reload UI')
        self.reloadButton.clicked.connect(self.reloadUI)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.nameLabel)
        self.mainLayout.addLayout(self.screenSelectionLayout)
        self.mainLayout.addWidget(self.reloadButton)

        # The main layout is established
        self.setLayout(self.mainLayout)

@QFlow.screen(
    name='secondaryScreen',
    autoreloadUI=True,
    parentType=QFlow.Window
)
# The class is initialized with predefined arguments using the decorator corresponding to the class
class QFlowSecondaryScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        """
        The 'parent' argument is added to the predefined arguments using the 
        'args' property on each object using the 'screen' decorator.
        """
        # The arguments are passed to super init
        super().__init__(**self.args)
    
    def UI(self):
        """
        Function where the entire screen UI is executed and must be initialized
        """
        self.label = QLabel('Hello!')
        self.nameLabel = QLabel(f'Screen: {self.name}')
        self.reloadButton = QPushButton('Reload UI')
        self.reloadButton.clicked.connect(self.reloadUI)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.nameLabel)
        self.mainLayout.addWidget(self.reloadButton) 

        # The main layout is established
        self.setLayout(self.mainLayout)

@QFlow.screen(
    name='secondMovementScreen',
    autoreloadUI=True
)
# The class is initialized with predefined arguments using the decorator corresponding to the class
class QFlowSecondMovementScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        """
        The 'parent' argument is added to the predefined arguments using the 
        'args' property on each object using the 'screen' decorator.
        """
        # The arguments are passed to super init
        super().__init__(**self.args)
    
    def UI(self):
        """
        Function where the entire screen UI is executed and must be initialized
        """

        self.nameLabel = QLabel(f'Screen: {self.name}')
        self.reloadButton = QPushButton('Go back')
        self.reloadButton.clicked.connect(self.parent().goBack)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.nameLabel)
        self.mainLayout.addWidget(self.reloadButton) 

        # The main layout is established
        self.setLayout(self.mainLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QFlowApp()
    window.run(QApp=app)