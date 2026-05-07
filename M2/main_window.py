from diakont_test_task.common.M.common_window import CommonWindow
from diakont_test_task.M2.widgets.main_panel import MainPanel

class MainWindow(CommonWindow):
    def __init__(self):
        super().__init__("M2", MainPanel())