import QFlow
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from dataclasses import dataclass
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

@QFlow.mainWindow('Main Window', [100, 100, 600, 400], QIcon())
@QFlow.style(style)
@QFlow.useConfig(config)
@QFlow.useSessionStorage()
class MyApp(QFlow.MainWindow):
    def __init__(self):
        super().__init__()
        self.Config: Config
        self.SessionStorage: QFlow.SessionStorage

        mainScreen = MainScreen(self)
        otherScreen = OtherScreen(self)
        storeScreen = StoreScreen(self)
        self.cls.addScreen(mainScreen)
        self.cls.addScreen(otherScreen)
        self.cls.addScreen(storeScreen)

        self.cls.setScreen(mainScreen.cls.name)

        self.cls.createWindow(PopupWindow(self))
        self.cls.createWindow(OtherPopupWindow(self))
        self.cls.createWindow(IndependentWindow())

@QFlow.screen('main')
@QFlow.useConfig(config)
@QFlow.useSessionStorage()
class MainScreen(QFlow.Screen):
    def __init__(self, parent):
        super().__init__(parent)
        self.Config: Config
        self.SessionStorage: QFlow.SessionStorage
        self.widgetParent = parent
        self.UI(parent)

    def UI(self, parent: QFlow.typing.MainWindowTyping) -> None:
        layout = QVBoxLayout()

        label = QLabel('Main Screen')
        label.setAlignment(Qt.AlignCenter)

        self.SessionStorage.setItem('test<1>', 'hello world!')
        sessionLabel = QLabel(f"Session data: {self.SessionStorage.getItem('test<1>')}")
        sessionLabel.setAlignment(Qt.AlignCenter)

        configLabel = QLabel(f'Configuration data: {self.Config.message}')
        configLabel.setAlignment(Qt.AlignCenter)

        buttonNotify = QPushButton('Show Notification')
        buttonNotify.clicked.connect(lambda: QFlow.components.Notify('This is a notification!', 3000, parent))

        buttonNavigate = QPushButton('Go to Other Screen')
        buttonNavigate.clicked.connect(lambda: parent.setScreen('other'))
        
        buttonStore = QPushButton('Go to Store Screen')
        buttonStore.clicked.connect(lambda: parent.setScreen('store'))

        buttonPopup = QPushButton('Open Popup')
        buttonPopup.clicked.connect(lambda: parent.createWindow(PopupWindow(parent)))

        buttonClosePopup = QPushButton('Close Popup')
        buttonClosePopup.clicked.connect(lambda: parent.closeWindow(PopupWindow(parent).cls.name))

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

        self.setLayout(layout)

@QFlow.screen('other', autoreloadUI=True)
@QFlow.useSessionStorage()
class OtherScreen(QFlow.Screen):
    def __init__(self, parent):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage
        self.widgetParent = parent
        self.UI(parent)

    def UI(self, parent: QFlow.MainWindowTyping) -> None:
        layout = QVBoxLayout()

        label = QLabel('Other Screen')
        label.setAlignment(Qt.AlignCenter)

        sessionLabel = QLabel(f"Session data test<1>: {self.SessionStorage.getItem('test<1>')}")
        sessionLabel.setAlignment(Qt.AlignCenter)

        sessionTestReload = QLabel(f"Session data test<2>: {self.SessionStorage.getItem('test<2>')}")
        sessionTestReload.setAlignment(Qt.AlignCenter)

        buttonReloadUI = QPushButton('Reload UI')
        buttonReloadUI.clicked.connect(self.cls.reloadUI)

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
        self.widgetParent = parent
        
        self.count, self.setCount, self.subscribeCount = useState(0)
        self.text, self.setText, self.subscribeText = useState("Hello from useState!")
        
        counter.subscribe(self.onCounterChange)
        
        self.UI(parent)
        
        self.subscribeCount(self.onCountChange)
        self.subscribeText(self.onTextChange)
        
        self.countLabel.setText(f"Count: {self.count()}")
        self.textLabel.setText(f"Text: {self.text()}")
        self.counterLabel.setText(f"Counter: {counter.value}")

    def UI(self, parent: QFlow.typing.MainWindowTyping) -> None:
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
        buttonBack = QPushButton('Go Back to Main Screen')
        buttonBack.clicked.connect(lambda: parent.setScreen('main'))
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
        QFlow.components.Notify(f"Count changed to {newValue}", 1000, self.widgetParent)
    
    def onTextChange(self, newValue):
        self.textLabel.setText(f"Text: {newValue}")
    
    def onCounterChange(self, newValue):
        self.counterLabel.setText(f"Counter: {newValue}")
        QFlow.components.Notify(f"Counter changed to {newValue}", 1000, self.widgetParent)

@QFlow.window('popup', 'Popup Window', [710, 100, 400, 150], QIcon(), resizable=False, animatedEvents={'fadeOut': True, 'fadeIn': True})
@QFlow.useSessionStorage()
class PopupWindow(QFlow.Window):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage
        self.mainWindow: QFlow.typing.MainWindowTyping = parent

        self.mainScreen = PopupMainScreen(self)
        self.cls.addScreen(self.mainScreen)
        self.cls.setScreen(self.mainScreen.cls.name)

    def closePopup(self):
        self.mainWindow.closeWindow(self.cls.name)

@QFlow.screen('popup-main')
@QFlow.useSessionStorage()
class PopupMainScreen(QFlow.Screen):
    def __init__(self, parent):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage
        self.widgetParent = parent
        self.UI(parent)

    def UI(self, parent: QFlow.typing.MainWindowTyping) -> None:
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
        QFlow.components.Notify(f'Session data: {value}', 3000, self.widgetParent)

@QFlow.window('otherpopup', 'Other Popup Window', [710, 285, 400, 150], QIcon(), resizable=False)
@QFlow.useSessionStorage()
class OtherPopupWindow(QFlow.Window):
    def __init__(self, parent):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage
        self.mainWindow: QFlow.typing.MainWindowTyping = parent

        self.mainScreen = OtherNoneScreen(self)
        self.cls.addScreen(self.mainScreen)
        self.cls.setScreen(self.mainScreen.cls.name)

    def closePopup(self):
        self.mainWindow.closeWindow(self.cls.name)

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

@QFlow.window('independent-window', 'Independent Window', [710, 470, 400, 150], QIcon(), resizable=False)
@QFlow.style(independentStyle)
@QFlow.useSessionStorage()
class IndependentWindow(QFlow.Window):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.SessionStorage: QFlow.SessionStorage

        self.mainScreen = OtherSimpleNoneScreen(self)
        self.otherScreen = OtherNoneScreen(self)

        self.cls.addScreen(self.mainScreen)
        self.cls.addScreen(self.otherScreen)
        self.cls.setScreen(self.mainScreen.cls.name)

@QFlow.screen('other-none', autoreloadUI=True)
@QFlow.useSessionStorage()
class OtherNoneScreen(QFlow.Screen):
    def __init__(self, parent):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage
        self.widgetParent = parent
        self.mainLayout = None
        self.UI(parent)

    def UI(self, parent: QFlow.typing.MainWindowTyping = None) -> None:
        self.mainLayout = QVBoxLayout()

        label = QLabel('Other-none Screen')
        label.setAlignment(Qt.AlignCenter)

        buttonReloadUI = QPushButton('Reload UI')
        buttonReloadUI.clicked.connect(self.cls.reloadUI)

        self.mainLayout.addWidget(label)
        self.mainLayout.addWidget(buttonReloadUI)

        self.setLayout(self.mainLayout)

@QFlow.screen('other-screen', autoreloadUI=True)
@QFlow.useSessionStorage()
class OtherSimpleNoneScreen(QFlow.Screen):
    def __init__(self, parent):
        super().__init__(parent)
        self.SessionStorage: QFlow.SessionStorage
        self.widgetParent = parent
        self.mainLayout = None
        self.UI(parent)

    def UI(self, parent: QFlow.typing.MainWindowTyping = None) -> None:
        self.mainLayout = QVBoxLayout()

        label = QLabel('Other-none Screen')
        label.setAlignment(Qt.AlignCenter)

        buttonReloadUI = QPushButton('Reload UI')
        buttonReloadUI.clicked.connect(self.cls.reloadUI)

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
    sys.exit(app.exec_())