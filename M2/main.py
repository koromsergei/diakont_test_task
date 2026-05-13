import sys
from PyQt5.QtWidgets import QApplication
from M2.main_window import MainWindow

app = QApplication(sys.argv)

window = MainWindow()

window.show()
app.exec_()