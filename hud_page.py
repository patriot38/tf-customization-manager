from PySide6.QtCore import Slot

import installer
from page_base import *
from hud_container import HudContainer

MAX_HUDS_ON_PAGE = 10


class HudPage(PageBase):

    def __init__(self):
        super().__init__('HUDs', HUD_DB_LINK, HUD_DB_FILE_NAME)

    def create_options_part(self):
        super().create_options_part()

        del_hud = QPushButton('Delete')
        del_hud.setIcon(QIcon('img/del.png'))
        del_hud.clicked.connect(self.on_del_installed_hud_btn_clicked)

        self.inst_hud_label = QLabel('Installed HUD:\nNone')
        self.update_installed_hud_info()

        installed_hud_layout = QHBoxLayout()
        installed_hud_layout.setAlignment(QtCore.Qt.AlignCenter)
        installed_hud_layout.addWidget(self.inst_hud_label)
        installed_hud_layout.addWidget(del_hud)

        self.options_layout.addLayout(installed_hud_layout)
        self.options_layout.addSpacing(80)

    def load_db(self):
        db = get_hud_db()
        for i in range(0, len(db), MAX_HUDS_ON_PAGE):
            layout = QVBoxLayout()
            for j in db[i:i + MAX_HUDS_ON_PAGE]:
                sc = HudContainer(self, *j)
                layout.addWidget(sc)

            page = QWidget()
            page.setLayout(layout)

            self.pages.append(page)
            # break  # << PROCESS ONLY 1 PAGE FOR DEBUG

        self.scroll_area.setWidget(self.pages[self.page_index])
        self.scroll_area.setWidgetResizable(True)

        get_time_since_mod('huds.json')
        d = 0
        self.refresh_label.setText(f'Last refresh:\n{d} days ago')

    @Slot()
    def on_del_installed_hud_btn_clicked(self):
        try:
            installer.del_installed_hud()
        except FileNotFoundError:
            pass
        self.update_installed_hud_info()

    def update_installed_hud_info(self):
        hud_name = config_vars['installed_hud'][0]
        self.inst_hud_label.setText('Installed HUD:\n{}'.format(hud_name))
