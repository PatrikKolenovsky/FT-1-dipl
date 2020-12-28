
from PyQt5 import QtCore, QtGui, QtWidgets
from ..model.Model import *
from ..view.AppView import *
class AppController:
    def __init__(self):
        self._app = QtWidgets.QApplication(sys.argv)
        self._model = Model()
        self._view = AppView()
        self.init()

    def init(self):
        self._view.verifySignal.connect(self.verify_credentials)

    def verify_credentials(self):
        self._model.username = self._view.username
        self._model.password = self._view.password
        self._view.clear()
        if self._model.verify_password():
            self._view.showMessage()
        else:
            self._view.showError()

    def run(self):
        self._view.show()
        return self._app.exec_()
