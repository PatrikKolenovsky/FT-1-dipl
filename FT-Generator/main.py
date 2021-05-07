import sys
from PyQt5.QtWidgets import QApplication
from view.appView import View
from controller.appController import Controller
from model.appModel import FtModel

ERROR_MSG = 'ERROR'

def setup():

    app = QApplication(sys.argv)
    # Show the calculator's GUI
    view = View()
    view.show()
    # Create instances of the model and the controller
    model = FtModel()
    controller = Controller(model=model, view=view)

    # Execute calculator's main loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    """Main function."""
    # Create an instance of `QApplication`
    setup()

