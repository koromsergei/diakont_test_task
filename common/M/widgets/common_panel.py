from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class CommonPanel(QWidget):
    def __init__(self):
        super().__init__() 
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.layout)
