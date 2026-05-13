import sys
from PyQt5.QtWidgets import QApplication
from M3.main_window import MainPanel

app = QApplication(sys.argv)

window = MainPanel()

window.show()
app.exec_()