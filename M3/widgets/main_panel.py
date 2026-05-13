from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QApplication
from common.M.widgets.common_panel import CommonPanel

import threading
from M3.serial_worker import connect_to_serial


class MainPanel(CommonPanel):
    message_pack_id_received = pyqtSignal(str)
    message_close_received = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.label = QLabel("0")
        self.layout.addWidget(self.label, alignment=Qt.AlignRight)

        self.message_pack_id_received.connect(self.on_server_pack_id)
        self.message_close_received.connect(self.on_close_requested)

        self.serial_thread = threading.Thread(
            target=connect_to_serial,
            args=(self.handle_server_pack_id, self.handle_close),
            daemon=True
        )
        self.serial_thread.start()

    def handle_server_pack_id(self, value):
        self.message_pack_id_received.emit(str(value))

    def handle_close(self, value):
        self.message_close_received.emit(bool(value))

    def on_server_pack_id(self, value):
        self.label.setText(str(value))

    def on_close_requested(self, value):
        if not value:
            app = QApplication.instance()
            if app is not None:
                app.quit()