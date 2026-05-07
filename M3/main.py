import sys
from PyQt5.QtWidgets import QApplication
from diakont_test_task.M3.main_window import MainWindow

app = QApplication(sys.argv)

window = MainWindow()

window.show()
app.exec_()