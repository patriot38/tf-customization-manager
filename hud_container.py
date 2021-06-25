from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from utils import *
import threading
import installer

from view_hud_window import ViewHudWindow

pixmap_of_loading = None

preview_imgs = []
func_started = False

HUD_PREVIEW_IMAGE_SIZE = (250, 135)


class HudContainer(QFrame):

    def __init__(self, parent_window, name, author, platforms: list, aspect_ratios: list, full_link: str,
                 download_link: str,
                 img_links: list[str]):
        super().__init__()
        self.parent_window = parent_window
        self.name = name
        self.author = author
        self.platforms = platforms
        self.aspect_ratios = aspect_ratios
        self.full_link = full_link
        self.download_link = download_link
        self.img_links = img_links
        self.imgs = []  # It will be used in future (ViewHudWindow will download imgs to this var)

        # Image
        # First, put the image of loading, then process the images in separate thread
        global pixmap_of_loading
        if not pixmap_of_loading:
            pixmap_of_loading = QPixmap()
            pixmap_of_loading.loadFromData(open('./img/loading.png', 'rb').read())
            pixmap_of_loading = pixmap_of_loading.scaled(*HUD_PREVIEW_IMAGE_SIZE)
        img_label = QLabel()
        img_label.setPixmap(pixmap_of_loading)

        # Process the images in separate thread
        def f():
            im = download_to_var(img_links[0])

            pixmap = QPixmap()
            pixmap.loadFromData(im)
            pixmap = pixmap.scaled(*HUD_PREVIEW_IMAGE_SIZE)

            img_label.setPixmap(pixmap)

        threading.Thread(target=f).start()

        # Labels
        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(QLabel('<html><head/><body><p><span style=" font-size:20pt; font-weight:600;">' + name),
                              alignment=Qt.AlignLeft)

        # Buttons
        view_btn = QPushButton('View')
        install_btn = QPushButton('Install')
        install_btn.clicked.connect(self.on_install_btn_clicked)

        view_btn.clicked.connect(self.on_view_btn_clicked)

        btns_layout = QHBoxLayout()
        btns_layout.addWidget(view_btn, stretch=False, alignment=Qt.AlignLeft)
        btns_layout.addWidget(install_btn, stretch=False, alignment=Qt.AlignLeft)

        vbox_layout.addWidget(QLabel('Aspect ratios: ' + ', '.join(aspect_ratios)))
        vbox_layout.addLayout(btns_layout, stretch=False)

        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignVCenter)
        main_layout.addWidget(img_label, alignment=Qt.AlignLeft, stretch=False)
        main_layout.addLayout(vbox_layout, stretch=False)

        main_layout.setSpacing(0)

        self.setLayout(main_layout)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

    @Slot()
    def on_install_btn_clicked(self):
        installer.install_hud(self.download_link, self.name)
        self.parent_window.update_installed_hud_info()

    @Slot()
    def on_view_btn_clicked(self):
        w = ViewHudWindow(self)
        w.show()
