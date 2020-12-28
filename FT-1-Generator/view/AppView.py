from functools import partial

from PyQt5 import QtWidgets, QtGui, QtCore


class AppView(QtWidgets.QWidget):
    verifySignal = QtCore.pyqtSignal()

    def __init__(self):
        super(AppView, self).__init__()
        self.username = ""
        self.password = ""
        self.initUi()

    def initUi(self):
        lay = QtWidgets.QVBoxLayout(self)
        title = QtWidgets.QLabel("<b>LOGIN</b>")
        lay.addWidget(title, alignment=QtCore.Qt.AlignHCenter)

        fwidget = QtWidgets.QWidget()
        flay = QtWidgets.QFormLayout(fwidget)
        self.usernameInput = QtWidgets.QLineEdit()
        self.usernameInput.textChanged.connect(partial(setattr, self, "username"))
        self.passwordInput = QtWidgets.QLineEdit(echoMode=QtWidgets.QLineEdit.Password)
        self.passwordInput.textChanged.connect(partial(setattr, self, "password"))
        self.loginButton = QtWidgets.QPushButton("Login")
        self.loginButton.clicked.connect(self.verifySignal)

        flay.addRow("Username: ", self.usernameInput)
        flay.addRow("Password: ", self.passwordInput)
        flay.addRow(self.loginButton)

        lay.addWidget(fwidget, alignment=QtCore.Qt.AlignHCenter)
        lay.addStretch()

    def clear(self):
        self.usernameInput.clear()
        self.passwordInput.clear()

    def showMessage(self):
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setText("your credentials are valid\n Welcome")
        messageBox.exec_()
        self.close()

    def showError(self):
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setText("your credentials are not valid\nTry again...")
        messageBox.setIcon(QtWidgets.QMessageBox.Critical)
        messageBox.exec_()
