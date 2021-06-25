import db_parser
from page_base import *
from sound_container import SoundContainer
from utils import play_sound_from_custom_dir
from installer import del_sound

MAX_SOUNDS_ON_PAGE = 10


class SoundPage(PageBase):

    def __init__(self):
        super().__init__('Sounds', SOUND_DB_LINK, SOUND_DB_FILE_NAME)

    def create_options_part(self):
        super().create_options_part()

        # Hitsound <Play>, <Delete>
        play_btn = QPushButton('Play')
        play_btn.setIcon(QIcon('img/play.png'))
        play_btn.clicked.connect(lambda: play_sound_from_custom_dir(True))

        del_btn = QPushButton('Delete')
        del_btn.setIcon(QIcon('img/del.png'))
        del_btn.clicked.connect(lambda: del_sound(True))

        frame_layout = QHBoxLayout()
        frame_layout.addWidget(play_btn)
        frame_layout.addWidget(del_btn)

        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setLayout(frame_layout)

        label = QLabel('Current hitsound')
        label.setAlignment(QtCore.Qt.AlignCenter)

        hs_vbox = QVBoxLayout()
        hs_vbox.addWidget(label)
        hs_vbox.addWidget(frame)

        hs_vbox.setAlignment(QtCore.Qt.AlignCenter)

        # Killsound <Play>, <Delete>
        play_btn = QPushButton('Play')
        play_btn.setIcon(QIcon('img/play.png'))
        play_btn.clicked.connect(lambda: play_sound_from_custom_dir(False))

        del_btn = QPushButton('Delete')
        del_btn.setIcon(QIcon('img/del.png'))
        del_btn.clicked.connect(lambda: del_sound(False))

        frame_layout = QHBoxLayout()
        frame_layout.addWidget(play_btn)
        frame_layout.addWidget(del_btn)

        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setLayout(frame_layout)

        label = QLabel('Current killsound')
        label.setAlignment(QtCore.Qt.AlignCenter)

        ks_vbox = QVBoxLayout()
        ks_vbox.addWidget(label)
        ks_vbox.addWidget(frame)

        ks_vbox.setAlignment(QtCore.Qt.AlignCenter)

        self.options_layout.addSpacing(30)
        self.options_layout.addLayout(hs_vbox)
        self.options_layout.addSpacing(30)
        self.options_layout.addLayout(ks_vbox)
        self.options_layout.setAlignment(QtCore.Qt.AlignCenter)

    def load_db(self):
        db = db_parser.get_sound_db()
        for i in range(0, len(db), MAX_SOUNDS_ON_PAGE):
            layout = QVBoxLayout()
            for j in db[i:i + MAX_SOUNDS_ON_PAGE]:
                sc = SoundContainer(*j)
                layout.addWidget(sc)

            page = QWidget()
            page.setLayout(layout)

            self.pages.append(page)
        self.scroll_area.setWidget(self.pages[self.page_index])
        self.scroll_area.setWidgetResizable(True)

        get_time_since_mod('sounds.csv')
        d = 0
        self.refresh_label.setText(f'Last refresh:\n{d} days ago')
