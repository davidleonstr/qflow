import os
import sys

os.environ['QT_API'] = 'pyqt6'

from qtpy.QtWidgets import (
    QApplication, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit
)
from qtpy.QtGui import QIcon

import QFlow

@QFlow.app(
    title='QFlow App Title', 
    geometry=[100, 100, 800, 600], 
    icon=lambda: QIcon(),
    animatedEvents={
        'fadeIn': True,
        'fadeOut': True
    }
)
class QFlowApp(QFlow.App):
    def __init__(self):
        # Definition of windows
        self.secondaryWindow = QFlowSecondaryWindow()

        # Definition of screens
        self.mainScreen = QFlowMainScreen(parent=self)
        self.secondMovementScreen = QFlowSecondMovementScreen(parent=self)

        # Adding screensThe main screen is set
        self.addScreen(screen=self.mainScreen)
        self.addScreen(screen=self.secondMovementScreen)

        # The main screen is set
        self.setScreen(name=self.mainScreen.name)

        # Creation of windows
        self.createWindow(self.secondaryWindow)

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
class QFlowSecondaryWindow(QFlow.Window):
    def __init__(self):
        """
        If you want to change any decorator argument at instance creation, 
        modify the argument dictionary (args).

        Example:
        >>> self.args['geometry'] = [2, 4, 8, 16]
        >>> self.args['parent'] = parent
        >>> super().__init__(**self.args)
        """
        # Definition of screens
        self.secondaryScreen = QFlowSecondaryScreen(self)

        # Adding screensThe main screen is set
        self.addScreen(screen=self.secondaryScreen)

        # The main screen is set
        self.setScreen(name=self.secondaryScreen.name)

@QFlow.screen(
    name='mainScreen',
    autoreloadUI=True,
    parentType=QFlow.App
)
class QFlowMainScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def effect(self):
        """
        It runs whenever the screen is mounted
        """
        pass
    
    def UI(self):
        self.label = QLabel('Hello!')
        self.nameLabel = QLabel(f'Screen: {self.name}')

        self.screenSelectionInput = QLineEdit()
        self.screenSelectionInput.setPlaceholderText('Screen Name')

        self.moveToButton = QPushButton('Move to')
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

        self.setLayout(self.mainLayout)

@QFlow.screen(
    name='secondaryScreen',
    autoreloadUI=True,
    parentType=QFlow.Window
)
class QFlowSecondaryScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def effect(self):
        """
        It runs whenever the screen is mounted
        """
        pass
    
    def UI(self):
        self.label = QLabel('Hello!')
        self.nameLabel = QLabel(f'Screen: {self.name}')
        self.reloadButton = QPushButton('Reload UI')
        self.reloadButton.clicked.connect(self.reloadUI)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.nameLabel)
        self.mainLayout.addWidget(self.reloadButton) 

        self.setLayout(self.mainLayout)

@QFlow.screen(
    name='secondMovementScreen',
    autoreloadUI=True
)
class QFlowSecondMovementScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def effect(self):
        """
        It runs whenever the screen is mounted
        """
        pass
    
    def UI(self):
        self.nameLabel = QLabel(f'Screen: {self.name}')
        self.reloadButton = QPushButton('Go back')
        self.reloadButton.clicked.connect(self.parent().goBack)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.nameLabel)
        self.mainLayout.addWidget(self.reloadButton) 

        self.setLayout(self.mainLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QFlowApp()
    window.run(QApp=app)