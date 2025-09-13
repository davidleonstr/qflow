import os
import sys
from dataclasses import dataclass

os.environ['QT_API'] = 'pyqt6'

# Using QtPy for Qt bindings abstraction
from qtpy.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon

import QFlow
from QFlow.stores import useState, Subscribeable

style = '''
QPushButton {
    background-color: #007BFF;
    color: white;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 14px;
    border: none;
}
QPushButton:hover {
    background-color: #0056b3; 
}
QPushButton:pressed {
    background-color: #004080;
}

QLabel {
    font-size: 16px;
    font-weight: semibold; 
}

QSpinBox, QLineEdit {
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
    font-size: 14px;
}
'''

@dataclass
class Config:
    message = 'hello world!'

config = Config()

counter = Subscribeable(0)

@QFlow.app('Main Window', [100, 100, 600, 520], lambda: QIcon('assets/icons/QFlow-white-icon.png'))
@QFlow.style(style)
@QFlow.insertConfig(config)
@QFlow.insertSessionStorage()
class MyApp(QFlow.App):
    def __init__(self):
        super().__init__()
        self.Config: Config
        self.SessionStorage: QFlow.typing.SessionStorage

        # Initialize screens with variables
        main_screen = MainScreen(self)
        other_screen = OtherScreen(self)
        store_screen = StoreScreen(self)
        
        self.typ.addScreen(main_screen)
        self.typ.addScreen(other_screen)
        self.typ.addScreen(store_screen)

        self.typ.setScreen(main_screen.typ.name)

        # Initialize windows with variables
        self.popupWindow = PopupWindow(self)
        other_popup_window = OtherPopupWindow(self)
        independent_window = IndependentWindow()

        self.typ.createWindow(self.popupWindow)
        self.typ.createWindow(other_popup_window)
        self.typ.createWindow(independent_window)

        # Get Qt framework info - will need to be adapted based on QFlow's getQtFramework function
        qt_info = "QtPy with available binding"
        QFlow.components.Notify(parent=self, message=f'Welcome to QFlow. {qt_info}.', type='info', customIcon=QFlow.Icon('assets/icons/QFlow-white-icon.png', 40, 40), duration=4000, delay=500)

@QFlow.screen('main', parentType=QFlow.App)
@QFlow.insertConfig(config)
@QFlow.insertSessionStorage()
class MainScreen(QFlow.Screen):
    def __init__(self, parent):
        super().__init__(parent)
        self.Config: Config
        self.SessionStorage: QFlow.SessionStorage
        self.UI()

    def __effect__(self):
        print(self.typ.parent().title, ':', 'The effect of the screen main')

    def UI(self) -> None:
        parent = self.typ.parent()

        layout = QVBoxLayout()

        label = QLabel('Main Screen')
        label.setAlignment(Qt.AlignCenter)

        self.SessionStorage.setItem('test<1>', 'hello world!')
        sessionLabel = QLabel(f"Session data: {self.SessionStorage.getItem('test<1>')}")
        sessionLabel.setAlignment(Qt.AlignCenter)

        configLabel = QLabel(f'Configuration data: {self.Config.message}')
        configLabel.setAlignment(Qt.AlignCenter)

        buttonNotify = QPushButton('Show Notification')
        buttonNotify.clicked.connect(lambda: QFlow.components.Notify('This is a notification!', 3000, parent=parent))

        buttonNavigate = QPushButton('Go to Other Screen')
        buttonNavigate.clicked.connect(lambda: parent.setScreen('other'))
        
        buttonStore = QPushButton('Go to Store Screen')
        buttonStore.clicked.connect(lambda: parent.setScreen('store'))

        buttonPopup = QPushButton('Open Popup')
        buttonPopup.clicked.connect(lambda: parent.createWindow(parent.popupWindow))

        buttonClosePopup = QPushButton('Close Popup')
        buttonClosePopup.clicked.connect(lambda: parent.closeWindow(parent.popupWindow.typ.name))

        dialogLayout = QVBoxLayout()
        dialogLayout.addWidget(QLabel('Hello in dialog.'))

        dialog = QFlow.components.Dialog(parent, dialogLayout)

        buttonDialog = QPushButton('Close Dialog')
        buttonDialog.clicked.connect(dialog.close)

        dialogLayout.addWidget(QPushButton('Hello'))

        dialog.addWidget(buttonDialog)

        buttonOpenDialog = QPushButton('Open Dialog')
        buttonOpenDialog.clicked.connect(dialog.show)

        buttonSetSessionData = QPushButton('Set test<2>')
        buttonSetSessionData.clicked.connect(lambda: self.SessionStorage.setItem('test<2>', 'hello world!'))

        reloadPopupScreens = QPushButton("Reload popup's screens")
        reloadPopupScreens.clicked.connect(lambda: parent.reloadWindowScreens('popup'))

        reloadPopupMainScreen = QPushButton("Reload popup's popup-main screen")
        reloadPopupMainScreen.clicked.connect(lambda: parent.reloadWindowScreen('popup', 'popup-main'))

        reloadScreens = QPushButton("Reload screens")
        reloadScreens.clicked.connect(parent.reloadScreens)
        
        layout.addWidget(label)
        layout.addWidget(configLabel)
        layout.addWidget(sessionLabel)
        layout.addWidget(buttonNotify)
        layout.addWidget(buttonNavigate)
        layout.addWidget(buttonStore)
        layout.addWidget(buttonPopup)
        layout.addWidget(buttonClosePopup)
        layout.addWidget(buttonOpenDialog)
        layout.addWidget(buttonSetSessionData)
        layout.addWidget(reloadPopupScreens)
        layout.addWidget(reloadPopupMainScreen)
        layout.addWidget(reloadScreens)

        self.setLayout(layout)

@QFlow.screen('other', autoreloadUI=True, parentType=QFlow.App)
@QFlow.insertSessionStorage()
class OtherScreen(QFlow.Screen):
    def __init__(self, parent):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage
        self.UI()

    def UI(self) -> None:
        parent = self.typ.parent()

        layout = QVBoxLayout()

        label = QLabel('Other Screen')
        label.setAlignment(Qt.AlignCenter)

        sessionLabel = QLabel(f"Session data test<1>: {self.SessionStorage.getItem('test<1>')}")
        sessionLabel.setAlignment(Qt.AlignCenter)

        sessionTestReload = QLabel(f"Session data test<2>: {self.SessionStorage.getItem('test<2>')}")
        sessionTestReload.setAlignment(Qt.AlignCenter)

        buttonReloadUI = QPushButton('Reload UI')
        buttonReloadUI.clicked.connect(self.typ.reloadUI)

        buttonBack = QPushButton('Go Back to Main Screen')
        buttonBack.clicked.connect(lambda: parent.setScreen('main'))
        
        buttonStore = QPushButton('Go to Store Screen')
        buttonStore.clicked.connect(lambda: parent.setScreen('store'))

        buttonShowNotifyWithItems = QPushButton('Show Notify with items')
        buttonShowNotifyWithItems.clicked.connect(
            lambda: QFlow.components.Notify(
                'Hello, I have items', 
                parent=parent, 
                items=[QPushButton('Hello')], type='info'
            )
        )

        layout.addWidget(label)
        layout.addWidget(sessionLabel)
        layout.addWidget(sessionTestReload)
        layout.addWidget(buttonBack)
        layout.addWidget(buttonStore)
        layout.addWidget(buttonReloadUI)
        layout.addWidget(buttonShowNotifyWithItems)

        self.setLayout(layout)

@QFlow.screen('store')
class StoreScreen(QFlow.Screen):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.count, self.setCount, self.subscribeCount, _ = useState(0)
        self.text, self.setText, self.subscribeText, _ = useState("Hello from useState!")
        
        counter.subscribe(self.onCounterChange)
        
        self.UI()
        
        self.subscribeCount(self.onCountChange)
        self.subscribeText(self.onTextChange)
        
        self.countLabel.setText(f"Count: {self.count()}")
        self.textLabel.setText(f"Text: {self.text()}")
        self.counterLabel.setText(f"Counter: {counter.value}")

    def UI(self) -> None:
        parent = self.typ.parent()

        mainLayout = QVBoxLayout()
        
        title = QLabel('Store Examples')
        title.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(title)
        
        useStateSection = QVBoxLayout()
        useStateTitle = QLabel('useState Example')
        useStateTitle.setAlignment(Qt.AlignCenter)
        useStateSection.addWidget(useStateTitle)
        
        countLayout = QHBoxLayout()
        self.countLabel = QLabel(f"Count: {self.count()}")
        countButton = QPushButton("Increment Count")
        countButton.clicked.connect(self.incrementCount)
        countLayout.addWidget(self.countLabel)
        countLayout.addWidget(countButton)
        useStateSection.addLayout(countLayout)
        
        textLayout = QHBoxLayout()
        self.textLabel = QLabel(f"Text: {self.text()}")
        textInput = QLineEdit(self.text())
        textInput.textChanged.connect(self.setText)
        textLayout.addWidget(self.textLabel)
        textLayout.addWidget(textInput)
        useStateSection.addLayout(textLayout)
        
        mainLayout.addLayout(useStateSection)
        
        subscribeableSection = QVBoxLayout()
        subscribeableTitle = QLabel('Subscribeable Example')
        subscribeableTitle.setAlignment(Qt.AlignCenter)
        subscribeableSection.addWidget(subscribeableTitle)
        
        counterLayout = QHBoxLayout()
        self.counterLabel = QLabel(f"Counter: {counter.value}")
        counterButton = QPushButton("Increment Counter")
        counterButton.clicked.connect(self.incrementCounter)
        counterLayout.addWidget(self.counterLabel)
        counterLayout.addWidget(counterButton)
        subscribeableSection.addLayout(counterLayout)
        
        mainLayout.addLayout(subscribeableSection)
        
        navLayout = QHBoxLayout()
        buttonBack = QPushButton('Go Back')
        buttonBack.clicked.connect(parent.goBack)
        buttonOther = QPushButton('Go to Other Screen')
        buttonOther.clicked.connect(lambda: parent.setScreen('other'))
        navLayout.addWidget(buttonBack)
        navLayout.addWidget(buttonOther)
        mainLayout.addLayout(navLayout)
        
        self.setLayout(mainLayout)
    
    def incrementCount(self):
        self.setCount(self.count() + 1)
    
    def incrementCounter(self):
        counter.value = counter.value + 1
    
    def onCountChange(self, newValue):
        self.countLabel.setText(f"Count: {newValue}")
        QFlow.components.Notify(f"Count changed to {newValue}", 1000, parent=self.parent())
    
    def onTextChange(self, newValue):
        self.textLabel.setText(f"Text: {newValue}")
    
    def onCounterChange(self, newValue):
        self.counterLabel.setText(f"Counter: {newValue}")
        QFlow.components.Notify(f"Counter changed to {newValue}", 1000, parent=self.parent())

@QFlow.window('popup', 'Popup Window', [710, 100, 400, 150], lambda: QIcon('assets/icons/QFlow-white-icon.png'), resizable=False, animatedEvents={'fadeOut': True, 'fadeIn': True}, parentType=QFlow.App)
@QFlow.insertSessionStorage()
class PopupWindow(QFlow.Window):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage

        # Initialize screen with variable
        self.mainScreen = PopupMainScreen(self)
        self.typ.addScreen(self.mainScreen)
        self.typ.setScreen(self.mainScreen.typ.name)

    def __effect__(self) -> None:
        independent_window_of_popup = IndependentWindow(self)
        independent_window_of_popup.typ.title = 'Dependent of Popup Window'
        independent_window_of_popup.typ.windowGeometry = [150, 300, 400, 150]
        self.typ.createWindow(independent_window_of_popup)

    def closePopup(self):
        self.typ.parent().closeWindow(self.typ.name)

@QFlow.screen('popup-main')
@QFlow.insertSessionStorage()
class PopupMainScreen(QFlow.Screen):
    def __init__(self, parent):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage
        self.UI()

    def UI(self) -> None:
        parent = self.typ.parent()

        mainLayout = QVBoxLayout()

        label = QLabel('This is a popup window')
        label.setAlignment(Qt.AlignCenter)

        buttonClose = QPushButton('Close Popup')
        buttonClose.clicked.connect(parent.closePopup)

        buttonGetSession = QPushButton('Get Session Data')
        buttonGetSession.clicked.connect(self.showSessionData)

        toggle = QFlow.components.ToggleSwitch(self, checked=True)

        mainLayout.addWidget(label)
        mainLayout.addWidget(buttonClose)
        mainLayout.addWidget(buttonGetSession)
        mainLayout.addWidget(toggle)

        self.setLayout(mainLayout)

    def showSessionData(self):
        value = self.SessionStorage.getItem('test<1>')
        QFlow.components.Notify(f'Session data: {value}', 3000, parent=self.parent())

@QFlow.window('otherpopup', 'Other Popup Window', [710, 285, 400, 150], lambda: QIcon('assets/icons/QFlow-white-icon.png'), resizable=False)
@QFlow.insertSessionStorage()
class OtherPopupWindow(QFlow.Window):
    def __init__(self, parent):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage

        # Initialize screen with variable
        self.mainScreen = OtherNoneScreen(self)
        self.typ.addScreen(self.mainScreen)
        self.typ.setScreen(self.mainScreen.typ.name)

    def closePopup(self):
        self.typ.parent().closeWindow(self.typ.name)

independentStyle = '''
QPushButton {
    background-color: #B22222; /* firebrick */
    color: white;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 14px;
    border: none;
}
QPushButton:hover {
    background-color: #8B1A1A; /* dark red hover */
}
QPushButton:pressed {
    background-color: #5C0A0A; /* even darker red */
}

QLabel {
    font-size: 16px;
    font-weight: semibold;
}

QSpinBox, QLineEdit {
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
    font-size: 14px;
}
'''

@QFlow.window('independent-window', 'Independent Window', [710, 470, 400, 150], lambda: QIcon('assets/icons/QFlow-white-icon.png'), resizable=False)
@QFlow.style(independentStyle)
@QFlow.insertSessionStorage()
class IndependentWindow(QFlow.Window):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.SessionStorage: QFlow.SessionStorage

        # Initialize screens with variables
        self.mainScreen = OtherSimpleNoneScreen(self)
        self.otherScreen = OtherNoneScreen(self)

        self.typ.addScreen(self.mainScreen)
        self.typ.addScreen(self.otherScreen)
        self.typ.setScreen(self.mainScreen.typ.name)

@QFlow.screen('other-none', autoreloadUI=True)
@QFlow.insertSessionStorage()
class OtherNoneScreen(QFlow.Screen):
    def __init__(self, parent):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage
        self.UI()

    def UI(self) -> None:
        self.mainLayout = QVBoxLayout()

        label = QLabel('Other-none Screen')
        label.setAlignment(Qt.AlignCenter)

        buttonReloadUI = QPushButton('Reload UI')
        buttonReloadUI.clicked.connect(self.typ.reloadUI)

        self.mainLayout.addWidget(label)
        self.mainLayout.addWidget(buttonReloadUI)

        self.setLayout(self.mainLayout)

@QFlow.screen('other-screen', autoreloadUI=True)
@QFlow.insertSessionStorage()
class OtherSimpleNoneScreen(QFlow.Screen):
    def __init__(self, parent):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage
        self.UI()

    def UI(self) -> None:
        parent = self.typ.parent()

        self.mainLayout = QVBoxLayout()

        label = QLabel('Other-none Screen')
        label.setAlignment(Qt.AlignCenter)

        buttonReloadUI = QPushButton('Reload UI')
        buttonReloadUI.clicked.connect(self.typ.reloadUI)

        goOtherNone = QPushButton('Go to other-none')
        goOtherNone.clicked.connect(lambda: parent.setScreen('other-none'))

        self.mainLayout.addWidget(label)
        self.mainLayout.addWidget(buttonReloadUI)
        self.mainLayout.addWidget(goOtherNone)

        self.setLayout(self.mainLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())