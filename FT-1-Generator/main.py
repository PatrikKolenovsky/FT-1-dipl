import sys
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets


class Model:
    def __init__(self):
        self.inputFile = ""
        self.outputFile = ""
        self.maskSize = 0



class View(QtWidgets.QWidget):
    verifySignal = QtCore.pyqtSignal()

    def __init__(self):
        super(View, self).__init__()
        self.initUi()

    def initUi(self):
        lay = QtWidgets.QVBoxLayout(self)
        title = QtWidgets.QLabel("<b>FT-1 Generator</b>")

        lay.addWidget(title, alignment=QtCore.Qt.AlignHCenter)

        fwidget = QtWidgets.QWidget()
        flay = QtWidgets.QFormLayout(fwidget)
        self.inputFileDir = QtWidgets.QLineEdit()
        self.inputFileDir.textChanged.connect(partial(setattr, self, "inputFile"))
        self.outputFileDir = QtWidgets.QLineEdit(echoMode=QtWidgets.QLineEdit.Password)
        self.outputFileDir.textChanged.connect(partial(setattr, self, "outputFile"))

        self.generateButton = QtWidgets.QPushButton("Generate")
        self.generateButton.clicked.connect(self.verifySignal)

        flay.addRow("Input file dir: ", self.inputFileDir)
        flay.addRow("Output file dir: ", self.outputFileDir)
        flay.addRow(self.generateButton)

        lay.addWidget(fwidget, alignment=QtCore.Qt.AlignHCenter)
        lay.addStretch()

    def clear(self):
        self.inputFileDir.clear()
        self.outputFileDir.clear()

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


class Controller:
    def __init__(self):
        self._app = QtWidgets.QApplication(sys.argv)
        self._model = Model()
        self._view = View()
        self.init()

    def init(self):
        self._view.verifySignal.connect(self.verify_credentials)

    def verify_credentials(self):
        self._view.clear()

    def run(self):
        self._view.show()
        return self._app.exec_()


if __name__ == '__main__':
    c = Controller()
    sys.exit(c.run())