import os
import pathlib
import shutil
import threading
import zipfile

from PySide6 import QtCore
from PySide6.QtCore import *
from PySide6.QtWidgets import QDialog, QMessageBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QProgressBar, \
    QRadioButton

from globals import config_vars
from utils import download_file_to_disk


class SoundInstallationDialog(QDialog):

    def __init__(self):
        super().__init__(None)
        self.install_mode = None

        as_hs_btn = QPushButton('Hitsound')
        as_ks_btn = QPushButton('Killsound')

        as_hs_btn.clicked.connect(self.on_hs_btn_clicked)
        as_ks_btn.clicked.connect(self.on_ks_btn_clicked)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(as_hs_btn)
        buttons_layout.addWidget(as_ks_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('I should install the sound as...'))
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    @QtCore.Slot()
    def on_hs_btn_clicked(self):
        self.install_mode = 'hitsound.wav'
        self.close()

    @QtCore.Slot()
    def on_ks_btn_clicked(self):
        self.install_mode = 'killsound.wav'
        self.close()


class HudInstallationDialog:

    def progress_hook(self, blocks, bs, size):
        percent = int(blocks * bs / size * 100)
        if percent == 100:
            self.dialog.accept()
        self.progress_bar.setValue(percent)

    def show_download_ui(self):
        label = QLabel(
            '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">Downloading the HUD...')
        label.setAlignment(Qt.AlignHCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(500, 40)
        self.progress_bar.setRange(0, 100)

        main_layout = QVBoxLayout()
        main_layout.addWidget(label)
        main_layout.addWidget(self.progress_bar)

        self.dialog = QDialog()
        self.dialog.setLayout(main_layout)

    def show_choice(self, huds: list):
        self.dialog = QDialog()

        btns_layout = QVBoxLayout()
        self.radio_btns = []
        for i in huds:
            btn = QRadioButton(self.dialog)
            btn.setText(i)
            btns_layout.addWidget(btn)
            self.radio_btns.append(btn)

        label = QLabel(
            '<html><head/><body><p align="center"><span style=" font-size:22pt; font-weight:600;">Please choose what '
            'to install')
        label.setAlignment(Qt.AlignHCenter)

        btn = QPushButton('Continue')
        btn.clicked.connect(self.on_select_btn_clicked)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addLayout(btns_layout)
        layout.addWidget(btn, alignment=Qt.AlignRight)

        self.dialog.setLayout(layout)

    def show_copying_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(
            '<html><head/><body><p align="center"><span style=" font-size:22pt; '
            'font-weight:600;">Installing...\nPlease wait.'), alignment=Qt.AlignHCenter)

        self.dialog = QDialog()
        self.dialog.setLayout(layout)

    @Slot()
    def on_select_btn_clicked(self):
        self.selected_hud = -1
        for n, i in enumerate(self.radio_btns):
            if i.isChecked():
                self.selected_hud = n
                self.dialog.accept()
                return


def install_sound(link):
    sid = SoundInstallationDialog()
    sid.exec()
    if sid.install_mode:
        sounds_path = config_vars['tf_path'] + '/my_sounds/sound/ui/'
        dir = QDir(sounds_path)
        if not dir.exists():
            dir.mkpath(sounds_path)
        download_file_to_disk(link, sounds_path + sid.install_mode)
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Ay!')
        msg_box.setText("Don't forget to enable hit/killsounds in tf2!")
        msg_box.exec()


def del_sound(is_hitsound: bool):
    sound_name = 'killsound.wav'
    if is_hitsound:
        sound_name = 'hitsound.wav'
    f = QFile(config_vars['tf_path'] + '/my_sounds/sound/ui/' + sound_name)
    f.remove()


def install_hud(link: str, hud_name):
    # Delete an existing hud
    try:
        del_installed_hud()
    except FileNotFoundError:
        pass

    # Download the hud
    hid = HudInstallationDialog()
    hid.show_download_ui()
    file_name = link.split('/')[-1]
    threading.Thread(target=download_file_to_disk, args=(link, file_name, hid.progress_hook)).start()
    code = hid.dialog.exec()

    if code == 0:  # The user has closed the dialog
        return

    # Find all HUD dirs
    # file_name = 'Sunset-Hud-master.zip'
    zf = zipfile.ZipFile(file_name)
    p = zipfile.Path(zf)
    to_process = [p]
    hud_dirs = []
    while to_process:
        curr_path = to_process.pop(0)

        for i in curr_path.iterdir():
            if i.name == 'info.vdf':
                hud_dirs.append(i.parent)
                break
        else:  # Else search the hud in subfolders
            for i in curr_path.iterdir():
                if not i.is_file():
                    to_process.append(i)

    # Get the path_to_hud_folder (in archive) to our hud folder
    hud_dir_paths = []
    for i in range(len(hud_dirs)):
        hud_dir = hud_dirs[i]
        path_to_hud_folder = hud_dir.name
        while hud_dir.parent.name != hud_dir.name:
            path_to_hud_folder = hud_dir.parent.name + '/' + path_to_hud_folder
            hud_dir = hud_dir.parent
        path_to_hud_folder = path_to_hud_folder.lstrip('/') + '/'
        hud_dir_paths.append(path_to_hud_folder)

    # Get the choice
    n = 0
    if len(hud_dirs) > 1:
        hid.show_choice([i for i in hud_dir_paths])
        if hid.dialog.exec() == 0:
            return
        n = hid.selected_hud

    # ========== Install the HUD ===========
    hud_dir = hud_dirs[n]
    hud_folder_name = hud_dir.name
    # Copy all the needed files
    prefix = path_to_hud_folder
    out = pathlib.Path(config_vars['tf_path'] + hud_folder_name)
    for archive_item in zf.infolist():
        if archive_item.filename.startswith(prefix):
            destpath = out.joinpath(archive_item.filename[len(prefix):])

            if archive_item.is_dir():
                os.makedirs(destpath, exist_ok=True)
            else:
                with zf.open(archive_item) as source, open(destpath, 'wb') as dest:
                    shutil.copyfileobj(source, dest)

    config_vars['installed_hud'] = (hud_name, hud_folder_name)
    os.remove(file_name)
    msg_box = QMessageBox()
    msg_box.setWindowTitle('Done!')
    msg_box.setText("The hud has been successfully installed")
    msg_box.exec()


def del_installed_hud():
    hud_path = config_vars['tf_path'] + config_vars['installed_hud'][1]
    config_vars['installed_hud'] = ('None', 'None')
    shutil.rmtree(hud_path)
