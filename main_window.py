from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import *

from sound_page import SoundPage
from hud_page import HudPage
from cfg_page import CfgPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('img/logo.png'))
        self.resize(870, 600)
        self.setWindowTitle('Team Fortress Customization Manager')
        self.version = '0.0.1'

        # Upper part (buttons)
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setAlignment(QtCore.Qt.AlignCenter)

        buttons = (QtWidgets.QPushButton('HUD'),
                   QtWidgets.QPushButton('Sounds'),
                   QtWidgets.QPushButton('CFGs'))

        for i in buttons:
            buttons_layout.addWidget(i)

        get_info_btn = QPushButton('?')
        get_info_btn.setFixedSize(20, 20)
        get_info_btn.clicked.connect(self.show_info)

        # Lower part
        stacked_widget = QtWidgets.QStackedWidget()
        pages = [HudPage(), SoundPage(), CfgPage()]
        for i in pages:
            stacked_widget.addWidget(i)
        stacked_widget.setCurrentIndex(0)

        # Connect signals
        # The following code won't work [i always = (len(buttons) - 1)]
        # for i in range(len(buttons)):
        #     buttons[i].clicked.connect(lambda: stacked_widget.setCurrentIndex(i))
        buttons[0].clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        buttons[1].clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
        buttons[2].clicked.connect(lambda: stacked_widget.setCurrentIndex(2))

        main_layout = QtWidgets.QVBoxLayout()
        btns_layout2 = QHBoxLayout()
        btns_layout2.addLayout(buttons_layout)
        btns_layout2.addWidget(get_info_btn)

        main_layout.addLayout(btns_layout2)
        main_layout.addWidget(stacked_widget)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    @Slot()
    def show_info(self):

        label = QLabel('Version: ' + self.version + '\nStill beta!')

        github_page_btn = QPushButton('Visit Github page')
        github_page_btn.clicked.connect(
            lambda: QDesktopServices.openUrl('https://github.com/t1var/tf-customization-manager'))

        layout = QVBoxLayout()
        layout.addWidget(label, alignment=QtCore.Qt.AlignHCenter)
        layout.addWidget(github_page_btn)

        w = QDialog(self)
        w.setLayout(layout)
        w.exec()
