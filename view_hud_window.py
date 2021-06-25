from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QPixmap, QIcon, QDesktopServices
import threading

from utils import *

HUD_VIEW_IMG_SIZE = (850, 477)


class ViewHudWindow(QWidget):

    def __init__(self, hud_cont_instance):
        super().__init__(None)

        self.curr_page_index = 0
        self.hud_cont_instance = hud_cont_instance
        self.imgs = hud_cont_instance.imgs
        self.close()

        # If the images of the hud have not been downloaded we need to download them
        if not hud_cont_instance.imgs:
            self.load_imgs(hud_cont_instance.img_links)
        self.show_ui()

    def load_imgs(self, img_links):
        # Process the images in separate thread
        def f(link):
            im = download_to_var(link)

            pixmap = QPixmap()
            pixmap.loadFromData(im)
            pixmap = pixmap.scaled(*HUD_VIEW_IMG_SIZE)

            self.imgs.append(pixmap)

        f(img_links[0])
        for i in img_links[1:]:  # The 1st picture is the preview image
            threading.Thread(target=f, args=[i]).start()

    def show_ui(self):
        prev_img_btn = QPushButton()
        self.img_shower = QLabel()
        next_img_btn = QPushButton()

        prev_img_btn.setIcon(QIcon('img/prev.png'))
        next_img_btn.setIcon(QIcon('img/next.png'))

        prev_img_btn.clicked.connect(lambda: self.display_picture(self.curr_page_index - 1))
        next_img_btn.clicked.connect(lambda: self.display_picture(self.curr_page_index + 1))

        img_showing_layout = QHBoxLayout()
        img_showing_layout.addWidget(prev_img_btn, alignment=Qt.AlignLeft | Qt.AlignHCenter, stretch=False)
        img_showing_layout.addWidget(self.img_shower)
        img_showing_layout.addWidget(next_img_btn, alignment=Qt.AlignRight | Qt.AlignHCenter)

        download_btn = QPushButton('Download')
        download_btn.setIcon(QIcon('img/download.png'))
        visit_full_page_btn = QPushButton('Visit full page')
        close_btn = QPushButton('Close')

        download_btn.clicked.connect(lambda: self.hud_cont_instance.on_install_btn_clicked())
        visit_full_page_btn.clicked.connect(lambda: QDesktopServices.openUrl(self.hud_cont_instance.full_link))
        close_btn.clicked.connect(lambda x: self.close())

        down_btns_layout = QHBoxLayout()
        down_btns_layout.addWidget(download_btn, alignment=Qt.AlignLeft)
        down_btns_layout.addWidget(visit_full_page_btn, alignment=Qt.AlignHCenter)
        down_btns_layout.addWidget(close_btn, alignment=Qt.AlignRight)

        main_layout = QVBoxLayout()
        main_layout.addWidget(
            QLabel(
                '<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">' + self.hud_cont_instance.name),
            alignment=Qt.AlignHCenter | Qt.AlignTop, stretch=False)
        main_layout.addLayout(img_showing_layout, stretch=True)
        main_layout.addLayout(down_btns_layout)

        self.setLayout(main_layout)

        self.display_picture(0)

    def display_picture(self, page_index):
        if 0 <= page_index < len(self.imgs):
            self.curr_page_index = page_index
            self.img_shower.setPixmap(self.imgs[page_index])
