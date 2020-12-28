import sys
from PyQt5 import Qt
from .model.Model import *
from .controller.AppController import *
from .view.AppView import *


class App(Qt.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        self.main_ctrl = AppController(self.model)
        self.main_view = AppView(self.model, self.main_ctrl)
        self.main_view.show()