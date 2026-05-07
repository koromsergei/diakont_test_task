from PyQt5.QtWidgets import QMainWindow

class CommonWindow(QMainWindow):
    def __init__(self, title, central_widget):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(400, 200)

        self.setCentralWidget(central_widget)