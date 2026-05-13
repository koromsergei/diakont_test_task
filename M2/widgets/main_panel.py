from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QCheckBox, QLabel
from common.M.widgets.common_panel import CommonPanel
from common.M.config import EXCHANGE_TIME

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

        self.checkbox = QCheckBox("Exchange")
        self.checkbox.setEnabled(False)

        self.label = QLabel("Pack_id")
        self.label.setText("0")

        self.layout.addWidget(self.checkbox, alignment=Qt.AlignRight)
        self.layout.addWidget(self.label, alignment=Qt.AlignRight)

        self.message_pack_id_received.connect(self.on_server_pack_id)
        self.message_sock_received.connect(self.on_server_sock)
        self.message_serial_received.connect(self.on_server_ser)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_exchange_state)
        self.timer.start(EXCHANGE_TIME)

        self.socket_thread = threading.Thread(
            target=connect_to_socket,
            args=(self.handle_socket_connected,),
            daemon=True
        )

        self.serial_thread = threading.Thread(
            target=connect_to_serial,
            args=(self.handle_server_pack_id, self.handle_serial_connected),
            daemon=True
        )

        self.socket_thread.start()
        self.serial_thread.start()

    def handle_server_pack_id(self, value):
        if isinstance(value, bytes):
            value = str(int.from_bytes(value, byteorder="big"))
        else:
            value = str(value)
        self.message_pack_id_received.emit(value)

    def handle_socket_connected(self, value):
        self.message_sock_received.emit(bool(value))

    def handle_serial_connected(self, value):
        self.message_serial_received.emit(bool(value))

    def on_server_pack_id(self, value):
        if value is not None:
            self.label.setText(value)

    def on_server_sock(self, value):
        self.exchange_sock = value

    def on_server_ser(self, value):
        self.exchange_ser = value

    def update_exchange_state(self):
        self.checkbox.setChecked(self.exchange_sock and self.exchange_ser)