from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QCheckBox, QLabel
from diakont_test_task.common.M.widgets.common_panel import CommonPanel

import threading
from M2.serial_worker import connect_to_serial
from M2.socket_worker import connect_to_socket


class MainPanel(CommonPanel):
    message_pack_id_received = pyqtSignal(str)
    message_sock_received = pyqtSignal(bool)
    message_serial_received = pyqtSignal(bool)

    def __init__(self):
        super().__init__() 
        self.exchange_sock = False
        self.exchange_ser = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.set_check_box)
        self.message_pack_id_received.connect(self.on_server_pack_id)
        self.message_sock_received.connect(self.on_server_sock)
        self.message_serial_received.connect(self.on_server_ser)

        self.socket_thread = threading.Thread(
            target=connect_to_socket, 
            args=(
                  self.handle_server_pack_id,
                  self.is_connected_
                   ),
            daemon=True)
    
        self.serial_thread = threading.Thread(
            target=connect_to_serial, 
            args=(
                  self.is_connected
                   ),
            daemon=True)
        


        self.chechbox = QCheckBox("Exchange")
        self.chechbox.setEnabled(False)
        self.lable = QLabel("Pack_id")

        self.layout.addWidget(self.chechbox, alignment=Qt.AlignRight)
        self.layout.addWidget(self.lable, alignment=Qt.AlignRight)

    def handle_server_pack_id(self, flag):
        self.message_pack_id_received.emit(flag)

    def on_server_pack_id(self, value):
        if value is not None:
            self.label.setText(value)

    def on_server_sock(self, value):
        self.exchange_sock = value
    
    def on_server_ser(self, value):
        self.exchange_ser = value

    def set_check_box(self):
        self.chechbox.setChecked(self.exchange_sock and self.exchange_ser)