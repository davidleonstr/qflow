import os
import sys

os.environ['QT_API'] = 'pyqt6'

from qtpy.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QStackedWidget, QCheckBox, QComboBox,
    QSpinBox, QGroupBox, QListWidget,
)
from qtpy.QtCore import Qt

import QFlow
from QFlow.components import Notify, Dialog, ToggleSwitch, TitleBar
from QFlow.stores import State
from QFlow.injectors import style

# ── Global state ──────────────────────────────────────────────────────────────

counterState  = State(0)
logState      = State([])
progressState = State(0)

# ── Template ──────────────────────────────────────────────────────────────────

class DefaultTemplate(QFlow.Template):
    def __init__(self, parent):
        super().__init__(parent)

        self.titleBar = TitleBar(parent, title='QFlow Playground')

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.screens = QStackedWidget()
        self.screens.setObjectName('screens')

        self.mainLayout.addWidget(self.titleBar)
        self.mainLayout.addWidget(self.screens)
        self.setLayout(self.mainLayout)

# ── App ───────────────────────────────────────────────────────────────────────

@QFlow.app(
    name='App',
    title='QFlow Playground',
    geometry=[100, 50, 900, 650],
    customTemplate=DefaultTemplate,
    frameless=True,
)
@style(r'QMainWindow { border: 1px solid #3e3e42; }')
class QFlowApp(QFlow.App):
    def __init__(self):
        self.mainScreen     = MainScreen(parent=self)
        self.notifyScreen   = NotifyScreen(parent=self)
        self.dialogScreen   = DialogScreen(parent=self)
        self.stateScreen    = StateScreen(parent=self)
        self.windowScreen   = WindowScreen(parent=self)

        screens = [
            self.mainScreen, self.notifyScreen, self.dialogScreen,
            self.stateScreen, self.windowScreen,
        ]
        for screen in screens:
            self.addScreen(screen=screen)

        self.setScreen(name='main')

# ── Main screen (menu) ────────────────────────────────────────────────────────

@QFlow.screen(name='main', autoreloadUI=True, parentType=QFlow.App)
class MainScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        title = QLabel('What do you want to try?')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(16)

        menuItems = [
            ('Notifications',   'notify'),
            ('Dialogs',         'dialog'),
            ('Reactive state',  'state'),
            ('Windows',         'window'),
        ]

        for label, targetScreen in menuItems:
            btn = QPushButton(label)
            btn.setFixedWidth(220)
            btn.clicked.connect(lambda _, t=targetScreen: self.parent().setScreen(name=t))
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(16)

        appLabel = QLabel(f'Global application: {type(QFlow.globals.app)}')
        appLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(appLabel)

        self.setLayout(layout)

# ── Notifications screen ──────────────────────────────────────────────────────

@QFlow.screen(name='notify', autoreloadUI=True, parentType=QFlow.App)
class NotifyScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        msgInput = QLineEdit()
        msgInput.setPlaceholderText('Notification message...')
        msgInput.setText('Hello from QFlow!')

        typeCombo = QComboBox()
        typeCombo.addItems(['success', 'error', 'info'])

        colorCombo = QComboBox()
        colorCombo.addItems(['black', 'white'])

        posCombo = QComboBox()
        posCombo.addItems(['top-right', 'top-left', 'bottom-right', 'bottom-left'])

        durationSpin = QSpinBox()
        durationSpin.setRange(500, 10000)
        durationSpin.setSingleStep(500)
        durationSpin.setValue(3000)
        durationSpin.setSuffix(' ms')

        showProgressBar = QCheckBox('Show progress bar')
        showProgressBar.setChecked(True)

        def fireNotification():
            Notify(
                message=msgInput.text() or 'No message',
                type=typeCombo.currentText(),
                color=colorCombo.currentText(),
                position=posCombo.currentText(),
                duration=durationSpin.value(),
                toggleProgressBar=showProgressBar.isChecked(),
                parent=self.parent(),
            )

        fireBtn = QPushButton('Send notification')
        fireBtn.clicked.connect(fireNotification)

        backBtn = QPushButton('Back')
        backBtn.clicked.connect(lambda: self.parent().setScreen(name='main'))

        optionsGroup = QGroupBox('Options')
        optionsLayout = QVBoxLayout()

        fields = [
            ('Message:',   msgInput),
            ('Type:',      typeCombo),
            ('Color:',     colorCombo),
            ('Position:',  posCombo),
            ('Duration:',  durationSpin),
        ]
        for labelText, widget in fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(labelText))
            row.addWidget(widget)
            optionsLayout.addLayout(row)

        optionsLayout.addWidget(showProgressBar)
        optionsGroup.setLayout(optionsLayout)

        layout.addWidget(optionsGroup)
        layout.addWidget(fireBtn)
        layout.addStretch()
        layout.addWidget(backBtn)
        self.setLayout(layout)

# ── Dialogs screen ────────────────────────────────────────────────────────────

@QFlow.screen(name='dialog', autoreloadUI=True, parentType=QFlow.App)
class DialogScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        colorCombo = QComboBox()
        colorCombo.addItems(['black', 'white'])

        widthSpin  = QSpinBox()
        heightSpin = QSpinBox()
        widthSpin.setRange(150, 600);  widthSpin.setValue(300);  widthSpin.setSuffix(' px')
        heightSpin.setRange(100, 500); heightSpin.setValue(200); heightSpin.setSuffix(' px')

        resultLabel = QLabel('Waiting for dialog action...')
        resultLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        def openDialog():
            dialogLayout = QVBoxLayout()

            confirmLabel = QLabel('Do you confirm this action?')
            confirmLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

            btnRow = QHBoxLayout()
            confirmBtn = QPushButton('Confirm')
            cancelBtn  = QPushButton('Cancel')
            btnRow.addWidget(confirmBtn)
            btnRow.addWidget(cancelBtn)

            dialogLayout.addWidget(confirmLabel)
            dialogLayout.addLayout(btnRow)

            dlg = Dialog(
                parent=self.parent(),
                childrenLayout=dialogLayout,
                color=colorCombo.currentText(),
                fixedSize=[widthSpin.value(), heightSpin.value()],
            )

            confirmBtn.clicked.connect(lambda: (resultLabel.setText('Confirmed'), dlg.close()))
            cancelBtn.clicked.connect(lambda:  (resultLabel.setText('Cancelled'), dlg.close()))
            dlg.show()

        openBtn = QPushButton('Open dialog')
        openBtn.clicked.connect(openDialog)

        backBtn = QPushButton('Back')
        backBtn.clicked.connect(lambda: self.parent().setScreen(name='main'))

        optionsGroup = QGroupBox('Dialog options')
        optionsLayout = QVBoxLayout()
        for labelText, widget in [('Color:', colorCombo), ('Width:', widthSpin), ('Height:', heightSpin)]:
            row = QHBoxLayout()
            row.addWidget(QLabel(labelText))
            row.addWidget(widget)
            optionsLayout.addLayout(row)
        optionsGroup.setLayout(optionsLayout)

        layout.addWidget(optionsGroup)
        layout.addWidget(openBtn)
        layout.addWidget(resultLabel)
        layout.addStretch()
        layout.addWidget(backBtn)
        self.setLayout(layout)

# ── Reactive state screen ─────────────────────────────────────────────────────

@QFlow.screen(name='state', autoreloadUI=True, parentType=QFlow.App)
class StateScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Counter
        counterGroup = QGroupBox('Counter (QFlow.stores.State)')
        counterLayout = QVBoxLayout()

        counterDisplay = QLabel(f'Value: {counterState.get()}')
        counterDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        counterState.subscribe(lambda v: counterDisplay.setText(f'Value: {v}'))

        btnRow = QHBoxLayout()
        decBtn = QPushButton('-')
        incBtn = QPushButton('+')
        rstBtn = QPushButton('Reset')
        decBtn.clicked.connect(lambda: counterState.set(counterState.get() - 1))
        incBtn.clicked.connect(lambda: counterState.set(counterState.get() + 1))
        rstBtn.clicked.connect(lambda: counterState.set(0))
        for btn in [decBtn, incBtn, rstBtn]:
            btnRow.addWidget(btn)

        counterLayout.addWidget(counterDisplay)
        counterLayout.addLayout(btnRow)
        counterGroup.setLayout(counterLayout)

        # Reactive log
        logGroup = QGroupBox('Reactive log')
        logLayout = QVBoxLayout()

        logList = QListWidget()
        for entry in logState.get():
            logList.addItem(entry)

        def onLogChange(entries):
            logList.clear()
            for entry in entries:
                logList.addItem(entry)
            logList.scrollToBottom()

        logState.subscribe(onLogChange)

        logInput = QLineEdit()
        logInput.setPlaceholderText('Type something and press Enter...')

        def addLogEntry():
            text = logInput.text().strip()
            if text:
                logState.set(logState.get() + [f'{text}'])
                logInput.clear()

        logInput.returnPressed.connect(addLogEntry)

        clearBtn = QPushButton('Clear log')
        clearBtn.clicked.connect(lambda: logState.set([]))

        logLayout.addWidget(logList)
        logLayout.addWidget(logInput)
        logLayout.addWidget(clearBtn)
        logGroup.setLayout(logLayout)

        backBtn = QPushButton('Back')
        backBtn.clicked.connect(lambda: self.parent().setScreen(name='main'))

        layout.addWidget(counterGroup)
        layout.addWidget(logGroup)
        layout.addStretch()
        layout.addWidget(backBtn)
        self.setLayout(layout)

# ── Secondary windows screen ──────────────────────────────────────────────────

@QFlow.screen(name='window', autoreloadUI=True, parentType=QFlow.App)
class WindowScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        statusLabel = QLabel('No windows open.')
        statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titleInput = QLineEdit('Secondary window')
        widthSpin  = QSpinBox(); widthSpin.setRange(200, 800);  widthSpin.setValue(400); widthSpin.setSuffix(' px')
        heightSpin = QSpinBox(); heightSpin.setRange(150, 600); heightSpin.setValue(300); heightSpin.setSuffix(' px')

        windowCount = [0]

        def openWindow():
            windowCount[0] += 1
            windowName = f'win-{windowCount[0]}'
            windowTitle = titleInput.text() or 'Secondary window'

            win = SecondaryWindow()
            win.name           = windowName
            win.title          = windowTitle
            win.windowGeometry = [160, 160, widthSpin.value(), heightSpin.value()]

            self.parent().createWindow(win, args={
                'windowName': windowTitle,
                'openedBy': 'WindowScreen',
            })
            statusLabel.setText(f'Window "{windowTitle}" created (id: {windowName})')

        def closeAllWindows():
            for name in list(self.parent().getAllWindows().keys()):
                self.parent().closeWindow(name)
            statusLabel.setText('All windows closed.')
            windowCount[0] = 0

        openBtn     = QPushButton('Open new window')
        closeAllBtn = QPushButton('Close all')
        openBtn.clicked.connect(openWindow)
        closeAllBtn.clicked.connect(closeAllWindows)

        optionsGroup = QGroupBox('Window settings')
        optionsLayout = QVBoxLayout()
        for labelText, widget in [('Title:', titleInput), ('Width:', widthSpin), ('Height:', heightSpin)]:
            row = QHBoxLayout()
            row.addWidget(QLabel(labelText))
            row.addWidget(widget)
            optionsLayout.addLayout(row)
        optionsGroup.setLayout(optionsLayout)

        backBtn = QPushButton('Back')
        backBtn.clicked.connect(lambda: self.parent().setScreen(name='main'))

        layout.addWidget(optionsGroup)
        layout.addWidget(openBtn)
        layout.addWidget(closeAllBtn)
        layout.addWidget(statusLabel)
        layout.addStretch()
        layout.addWidget(backBtn)
        self.setLayout(layout)

# ── Secondary window ──────────────────────────────────────────────────────────

@QFlow.window(
    name='secondary',
    title='Secondary window',
    geometry=[160, 160, 400, 300],
    strictClosingWindows=False,
)
class SecondaryWindow(QFlow.Window):
    def __init__(self):
        self.screen = SecondaryScreen(self)
        self.addScreen(screen=self.screen)
        self.setScreen(name='secondaryScreen')

    def effect(self):
        self.params = QFlow.hooks.Params(self)
        title = self.params.get('windowName') or 'Secondary window'
        self.setWindowTitle(title)

@QFlow.screen(name='secondaryScreen', autoreloadUI=True)
class SecondaryScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        params = QFlow.hooks.Params(self.parent())
        info   = params.get()

        openedByLabel = QLabel(f"Opened by: {info.get('openedBy', '?')}")
        openedByLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        toggle      = ToggleSwitch(parent=self)
        toggleLabel = QLabel('Toggle: OFF')
        toggleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        def onTogglePress(event):
            ToggleSwitch.mousePressEvent(toggle, event)

            isOn = toggle.isChecked()
            toggleLabel.setText(f'Toggle: {'ON' if isOn else 'OFF'}')

        toggle.mousePressEvent = onTogglePress

        closeBtn = QPushButton('Close window')
        closeBtn.clicked.connect(self.parent().close)

        layout.addWidget(openedByLabel)
        layout.addSpacing(12)
        layout.addWidget(toggle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(toggleLabel)
        layout.addSpacing(12)
        layout.addWidget(closeBtn)
        self.setLayout(layout)

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app = QApplication(sys.argv)

    QFlow.globals.app = app

    window = QFlowApp()
    window.run(QApp=app)