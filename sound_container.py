from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6 import QtCore

from playsound import playsound
from installer import install_sound


class SoundContainer(QWidget):

    def __init__(self, name, author, download_link):
        super().__init__()
        self.download_link = download_link

        name = QLabel('<html><head/><body><p><span style=\" font-size:14pt; font-weight:100;\">' + name)
        author = QLabel("<html><head/><body><p>Author: " + author)

        labels_layout = QVBoxLayout()
        labels_layout.addWidget(name)
        labels_layout.addWidget(author)

        play_btn = QPushButton()
        install_btn = QPushButton()

        play_btn.setIcon(QIcon('img/play.png'))
        install_btn.setIcon(QIcon('img/install.png'))

        play_btn.clicked.connect(self.play_sound)
        install_btn.clicked.connect(self.install_sound)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(play_btn)
        buttons_layout.addWidget(install_btn)
        buttons_layout.setAlignment(Qt.AlignRight)

        main_layout = QHBoxLayout()
        main_layout.addLayout(labels_layout)
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    @QtCore.Slot()
    def play_sound(self):
        playsound(self.download_link)

    @QtCore.Slot()
    def install_sound(self):
        install_sound(self.download_link)
