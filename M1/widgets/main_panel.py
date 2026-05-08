from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QCheckBox, QLabel, QApplication
from diakont_test_task.common.M.widgets.common_panel import CommonPanel
import threading

from server import run_server

class MainPanel(CommonPanel):
    message_respond_received = pyqtSignal(bool)
    message_pack_id_received = pyqtSignal(str)
    message_closed_received = pyqtSignal(bool)

    def __init__(self):
        super().__init__() 

        self.chechbox = QCheckBox("respond")
        
        self.lable = QLabel("Pack_id")

        self.layout.addWidget(self.chechbox, alignment=Qt.AlignRight)
        self.layout.addWidget(self.lable, alignment=Qt.AlignRight)

        # тут определяется функция, которая вызывается при срабатывании сигнала
        self.message_respond_received.connect(self.on_server_respond)
        self.message_pack_id_received.connect(self.on_server_pack_id)
        self.message_closed_received.connect(self.on_server_closed)

        self.server_thread = threading.Thread(
            target=run_server, 
            args=(self.handle_server_respond,
                  self.handle_server_pack_id,
                  self.handle_server_closed
                   ),
            daemon=True)
        self.server_thread.start()


    def handle_server_respond(self, flag):
        # испускание сигнала, передача переменной в функцию
        self.message_respond_received.emit(flag)


    def handle_server_pack_id(self, flag):
        self.message_pack_id_received.emit(flag)


    def handle_server_closed(self, flag):
        self.message_closed_received.emit(flag)


    def on_server_respond(self, flag):
        self.chechbox.setEnabled(flag)


    def on_server_pack_id(self, value):
        if value is not None:
            self.lable.setText(value)
    

    def on_server_closed(self, value):
        if value:
            QApplication.instance().quit()