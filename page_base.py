from PySide6 import QtCore
from PySide6.QtWidgets import *
from db_parser import *
from PySide6.QtGui import QIcon


class PageBase(QWidget):

    def __init__(self, browser_name: str, db_link: str, db_name: str):
        super().__init__()
        self.browser_name = browser_name
        self.db_link = db_link
        self.db_name = db_name
        self.page_index = 0
        self.pages = []

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.create_options_part()
        self.create_browser_part()

        self.load_db()

    def create_options_part(self):
        self.options_layout = QVBoxLayout()

        # Refresh stuff
        refresh_db_btn = QPushButton('Refresh DB')
        refresh_db_btn.setIcon(QIcon('img/refresh.png'))
        refresh_db_btn.clicked.connect(self.refresh_db)

        self.refresh_label = QLabel('#LAST_REFRESH_TEXT')

        refresh_layout = QHBoxLayout()
        refresh_layout.setAlignment(QtCore.Qt.AlignCenter)
        refresh_layout.addWidget(self.refresh_label)
        refresh_layout.addWidget(refresh_db_btn)

        self.options_layout.addLayout(refresh_layout)

        self.main_layout.addLayout(self.options_layout)

    def create_browser_part(self):
        # Scroll area
        self.scroll_area = QScrollArea()

        # Page switching part [< Page #1 >]
        go_back_btn = QPushButton()
        go_forward_btn = QPushButton()
        self.page_label = QLabel('Page #1')

        go_back_btn.setIcon(QIcon('img/prev.png'))
        go_forward_btn.setIcon(QIcon('img/next.png'))

        go_back_btn.clicked.connect(self.show_prev_page)
        go_forward_btn.clicked.connect(self.show_next_page)

        page_switching_box = QHBoxLayout()
        page_switching_box.setAlignment(QtCore.Qt.AlignCenter)
        page_switching_box.addWidget(go_back_btn)
        page_switching_box.addWidget(self.page_label)
        page_switching_box.addWidget(go_forward_btn)

        # Add this to the layout
        browser_layout = QVBoxLayout()
        browser_layout.addWidget(QLabel(self.browser_name), alignment=QtCore.Qt.AlignCenter)
        browser_layout.addWidget(self.scroll_area)
        browser_layout.addLayout(page_switching_box)

        self.main_layout.addLayout(browser_layout)

    def load_db(self):
        pass

    @QtCore.Slot()
    def refresh_db(self):
        download_file_to_disk(self.db_link, self.db_name)
        self.load_db()

    @QtCore.Slot()
    def show_prev_page(self):
        if self.page_index - 1 >= 0:
            self.page_index -= 1
            self.scroll_area.takeWidget()  # Looks like without this Qt deletes the object
            self.scroll_area.setWidget(self.pages[self.page_index])
            self.page_label.setText('Page #' + str(self.page_index + 1))

    @QtCore.Slot()
    def show_next_page(self):
        if self.page_index + 1 < len(self.pages):
            self.page_index += 1
            self.scroll_area.takeWidget()
            self.scroll_area.setWidget(self.pages[self.page_index])
            self.page_label.setText('Page #' + str(self.page_index + 1))
