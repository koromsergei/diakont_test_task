from common.M.common_window import CommonWindow
from M2.widgets.main_panel import MainPanel

class MainWindow(CommonWindow):
    def __init__(self):
        super().__init__("M2", MainPanel())