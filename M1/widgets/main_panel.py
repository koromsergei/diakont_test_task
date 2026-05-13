from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QCheckBox, QLabel, QApplication
from common.M.widgets.common_panel import CommonPanel
from common.M.config import TIME_TO_CLOSE
import threading
from M1.server import run_server


class MainPanel(CommonPanel):
    message_respond_received = pyqtSignal(bool)
    message_pack_id_received = pyqtSignal(int)
    message_closed_received = pyqtSignal(bool)

    def __init__(self):
        super().__init__() 
        self.checkbox = QCheckBox("respond")
        self.checkbox.setChecked(True)
        self.timer = QTimer()
        self.timer.timeout.connect(self.close_all)
        self.label = QLabel("Pack_id")

        self.layout.addWidget(self.checkbox, alignment=Qt.AlignRight)
        self.layout.addWidget(self.label, alignment=Qt.AlignRight)

        self.message_respond_received.connect(self.on_server_respond)
        self.message_pack_id_received.connect(self.on_server_pack_id)
        self.message_closed_received.connect(self.on_server_closed)

        self.server_thread = threading.Thread(
            target=run_server, 
            args=(self.handle_server_respond,
                  self.handle_server_pack_id,
                  self.handle_server_closed,
                  self.send_respond
                   ),
            daemon=True)
        self.server_thread.start()
        self.checkbox.toggled.connect(self.on_checkbox_changed)

    
    def close_all(self):
        QApplication.instance().quit()
    
    def send_respond(self):
        return self.checkbox.isChecked()


    def on_checkbox_changed(self, checked):
        if not checked:
            self.timer.start(TIME_TO_CLOSE)
        else:
            self.timer.stop()


    def handle_server_respond(self, flag):
        self.message_respond_received.emit(flag)


    def handle_server_pack_id(self, flag):
        self.message_pack_id_received.emit(flag)


    def handle_server_closed(self, flag):
        self.message_closed_received.emit(flag)


    def on_server_respond(self, flag):
        self.checkbox.setEnabled(flag)


    def on_server_pack_id(self, value):
        if value is not None:
            self.label.setText(str(value))
    

    def on_server_closed(self, value):
        if value:
            QApplication.instance().quit()