from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QLabel
from diakont_test_task.common.M.widgets.common_panel import CommonPanel

class MainPanel(CommonPanel):
    def __init__(self):
        super().__init__() 
        self.attempt = 0
        self.sock = None
        self.ser = serial.Serial(
                    "COM3", 
                    COM_SPEED, 
                    bytesize=8,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=COM_TIMEOUT
        )
        QTimer.singleShot(0, self.connect_to_server)

        self.chechbox = QCheckBox("Exchange")
        self.chechbox.setEnabled(False)
        self.lable = QLabel("Pack_id")

        self.layout.addWidget(self.chechbox, alignment=Qt.AlignRight)
        self.layout.addWidget(self.lable, alignment=Qt.AlignRight)

