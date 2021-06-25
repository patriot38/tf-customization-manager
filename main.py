import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from request_tf_path_dialog import RequestTfPathDialog
from globals import *

if __name__ == "__main__":
    app = QApplication([])

    try:
        config_vars = load_config()
    except FileNotFoundError:
        r = RequestTfPathDialog()
        if not r.exec():
            sys.exit(-1)
        config_vars['tf_path'] = r.line_edit.text()
        config_vars['installed_hud'] = ('None', 'None')

    w = MainWindow()
    w.show()

    res = app.exec()
    save_config()

    sys.exit(res)
