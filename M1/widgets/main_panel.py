from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QLabel
from diakont_test_task.common.M.widgets.common_panel import CommonPanel

class MainPanel(CommonPanel):
    def __init__(self):
        super().__init__() 

        self.chechbox = QCheckBox("respond")
        
        self.lable = QLabel("Pack_id")

        self.layout.addWidget(self.chechbox, alignment=Qt.AlignRight)
        self.layout.addWidget(self.lable, alignment=Qt.AlignRight)


