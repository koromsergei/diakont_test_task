from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QCheckBox, QLabel
from diakont_test_task.common.M.widgets.common_panel import CommonPanel

import threading
from server import connect_to_server


class MainPanel(CommonPanel):
    message_pack_id_received = pyqtSignal(str)

    def __init__(self):
        super().__init__() 
        
        self.message_pack_id_received.connect(self.on_server_pack_id)

        self.server_thread = threading.Thread(
            target=connect_to_server, 
            args=(
                  self.handle_server_pack_id
                   ),
            daemon=True)
        
        def handle_server_pack_id(self, flag):
            self.message_pack_id_received.emit(flag)

        self.chechbox = QCheckBox("Exchange")
        self.chechbox.setEnabled(False)
        self.lable = QLabel("Pack_id")

        self.layout.addWidget(self.chechbox, alignment=Qt.AlignRight)
        self.layout.addWidget(self.lable, alignment=Qt.AlignRight)

