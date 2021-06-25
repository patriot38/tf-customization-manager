import datetime as dt
import tempfile
from os.path import getmtime
from urllib.request import urlretrieve as download_file_to_disk

import playsound
import requests

from globals import config_vars


def get_time_since_mod(path_to_file):
    """Returns time (in days) since the last modification of the file"""
    seconds_since_epoch = getmtime(path_to_file)
    d = dt.date.fromtimestamp(seconds_since_epoch)
    return (dt.date.today() - d).days


def play_sound_from_custom_dir(is_hitsound: bool):
    try:
        sound_name = 'killsound.wav'
        if is_hitsound:
            sound_name = 'hitsound.wav'
        playsound.playsound(config_vars['tf_path'] + '/my_sounds/sound/ui/' + sound_name)
    except playsound.PlaysoundException as e:
        print(e)


def download_to_var(link: str):
    return requests.get(link).content


def download_img_to_temp_file(link: str):
    temp = tempfile.TemporaryFile()
    temp.write(download_to_var(link))
    temp.seek(0)
    return temp
