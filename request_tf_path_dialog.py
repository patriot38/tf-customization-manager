from PySide6.QtCore import QDir
from PySide6 import QtCore
from PySide6.QtWidgets import *


class RequestTfPathDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.line_edit = QLineEdit()
        select_location_btn = QPushButton('Select location')
        ok_btn = QPushButton('OK')

        select_location_btn.clicked.connect(self.on_select_btn_clicked)
        ok_btn.clicked.connect(self.on_ok_btn_clicked)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.line_edit)
        h_layout.addWidget(select_location_btn)
        h_layout.addWidget(ok_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Sorry but I don't know where TF2 is located. Please type its location below"))
        main_layout.addLayout(h_layout)

        self.setLayout(main_layout)

    @QtCore.Slot()
    def on_select_btn_clicked(self):
        path = QFileDialog.getExistingDirectory(self, 'Select /tf/custom path', '~/')
        if path:
            self.line_edit.setText(path)

    @QtCore.Slot()
    def on_ok_btn_clicked(self):
        path = self.line_edit.text()
        d = QDir(path)
        if d.exists() and path.endswith('/tf/custom'):
            self.accept()
            self.line_edit.setText(path + '/')
            return
        QMessageBox.critical(self, 'Error', 'Sorry this path is not correct')
