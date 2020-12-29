from PyQt5.QtWidgets import QLineEdit, QLabel, QGridLayout, QPushButton, QMainWindow, QVBoxLayout, QWidget


class View(QMainWindow):
    """PyCalc's View (GUI)."""

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('FT-1 Generator')
        self.setFixedSize(800, 600)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the display and the buttons
        self._createDirectories()
        self._createButtons()

    # Snip
    def _createDirectories(self):
        """Create the buttons."""
        self.directories = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        directories = {
            '<h3>Input file:</h3>': (0, 1),
            'inputFileDir': (0, 2),
            '<h3>Output file:</h3>': (0, 3),
            'outputFileDir': (0, 4),
        }
        # Create the buttons and add them to the grid layout
        for btnText, pos in directories.items():
            if btnText == 'inputFileDir' or btnText == 'outputFileDir':
                self.directories[btnText] = QLineEdit()
            else:
                self.directories[btnText] = QLabel()
                self.directories[btnText].setText(btnText)
            self.directories[btnText].setFixedSize(100, 30)
            buttonsLayout.addWidget(self.directories[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)  # Snip

    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {
            'Generate': (0, 0),
        }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(100, 60)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)

    # Snip
    def setDisplayText(self, text):
        """Set display's text."""
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """Get display's text."""
        return self.display.text()

    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText('')
