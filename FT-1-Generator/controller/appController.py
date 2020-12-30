ERROR_MSG = 'ERROR'


class Controller:
    """App's Controller."""

    def __init__(self, model, view):
        """Controller initializer."""
        self._ftModel = model
        self._view = view
        # Connect signals and slots
        self._connectSignals()

    def _connectSignals(self):
        self._view.generateBtn.clicked.connect(self._generateFile)

    def _generateFile(self):
        input = self._view.directories['inputFileDir'].text()
        output = self._view.directories['outputFileDir'].text()
        maskSize = self._view.slider.value()
        print(input)
        print(output)
        print(maskSize)

        self._ftModel.transform(input, output, maskSize)
