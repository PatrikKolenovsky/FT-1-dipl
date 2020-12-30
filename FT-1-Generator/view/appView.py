from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLineEdit, QLabel, QGridLayout, QPushButton, QMainWindow, QVBoxLayout, QWidget, QSlider
from configuration.config import settings


class View(QMainWindow):
    """App's View (GUI)."""

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

        self._createDirectories()
        self._createSlide()
        self._createImage()
        self._createButtons()

    # Snip
    def _createDirectories(self):
        """Create the dirs."""
        self.directories = {}
        buttonsLayout = QGridLayout()
        # Dir text | position on the QGridLayout
        directories = {
            '<h3>Input file:</h3>': (0, 0),
            'inputFileDir': (0, 1),
            '<h3>Output file:</h3>': (0, 2),
            'outputFileDir': (0, 3),
        }
        # Create the buttons and add them to the grid layout
        for btnText, pos in directories.items():
            if btnText == 'inputFileDir':
                # settings.ROOT + "/files/"
                self.directories[btnText] = QLineEdit(settings.ROOT + "/files/sine.wav")
                self.directories[btnText].setFixedSize(180, 30)
            elif btnText == 'outputFileDir':
                # settings.ROOT + "/files/"
                self.directories[btnText] = QLineEdit(settings.ROOT + "/files/output.wav")
                self.directories[btnText].setFixedSize(180, 30)
            else:
                self.directories[btnText] = QLabel()
                self.directories[btnText].setText(btnText)
                self.directories[btnText].setFixedSize(70, 30)

            buttonsLayout.addWidget(self.directories[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)  # Snip

    def _createButtons(self):
        buttonsLayout = QGridLayout()

        self.generateBtn = QPushButton('Generate')
        self.generateBtn.setFixedSize(100, 60)
        buttonsLayout.addWidget(self.generateBtn)

        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)

    def _createSlide(self):
        self.maskSize = 0
        self.maskSizeSlider = 0
        slideLayout = QGridLayout()

        # Label
        self.slideLabel = QLabel()
        self.slideLabel.setText("<h3>Mask size:</h3>")
        self.slideLabel.setFixedSize(680, 30)
        slideLayout.addWidget(self.slideLabel, 0, 0)

        # Value Label
        self.slideValueLabel = QLabel()
        self.slideValueLabel.setText('<h3>5</h3>')
        self.slideValueLabel.setFixedSize(30, 30)
        slideLayout.addWidget(self.slideValueLabel, 2, 0)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setValue(5)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setFixedSize(310, 30)
        self.slider.valueChanged.connect(self.updateLabel)
        slideLayout.addWidget(self.slider, 1, 0)

        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(slideLayout)

    def _createImage(self):
        # Create input image
        self.image1 = QLabel()
        pixmap = QPixmap( settings.ROOT + "/image/404.png")
        self.image1.setPixmap(pixmap)
        self.image1.setAlignment(Qt.AlignRight)
        # self.image1..setFixedSize(250, 250)

        # Create input image
        self.image2 = QLabel()
        pixmap = QPixmap( settings.ROOT + "/image/404.png")
        self.image2.setPixmap(pixmap)
        self.image2.setAlignment(Qt.AlignLeft)
        # self.image1..setFixedSize(250, 250)


        imageLayout = QGridLayout()
        imageLayout.addWidget(self.image1, 0, 0)
        imageLayout.addWidget(self.image2, 0, 0)

        self.generalLayout.addLayout(imageLayout)

    def updateLabel(self, value):
        self.slideValueLabel.setText('<h3>' + str(value) + '</h3>')

    # def setDisplayText(self, text):
    #     """Set display's text."""
    #     self.display.setText(text)
    #     self.display.setFocus()

    # def displayText(self):
    #     """Get display's text."""
    #     return self.display.text()
    #
    # def clearDisplay(self):
    #     """Clear the display."""
    #     self.setDisplayText('')
