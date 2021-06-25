from csv import reader
from utils import *
import json

from platform import system

host_os = system()
if host_os == 'Darwin':
    host_os = 'Mac'

SOUND_DB_FILE_NAME = 'sounds.csv'
SOUND_DB_LINK = "https://raw.githubusercontent.com/t1var/tfcm-databases/master/sounds.csv"

HUD_DB_FILE_NAME = 'huds.json'
HUD_DB_LINK = 'https://raw.githubusercontent.com/t1var/tfcm-databases/main/huds.json'

CFG_DB_FILE_NAME = 'cfgs.csv'
CFG_DB_LINK = ''


def get_sound_db():
    try:
        with open(SOUND_DB_FILE_NAME) as f:
            r = reader(f, delimiter=';')
            next(r)
            return [i for i in r]
    except FileNotFoundError:
        print('Downloading sound db...')
        download_file_to_disk(SOUND_DB_LINK, SOUND_DB_FILE_NAME)
        return get_sound_db()


def get_hud_db():
    try:
        with open(HUD_DB_FILE_NAME) as f:
            db = json.load(f)

        # Filter the DB
        res = []
        for i in db:
            supported_oses = i[2]
            if host_os in supported_oses:
                res.append(i)
        return res

    except FileNotFoundError:
        print('Downloading hud db...')
        download_file_to_disk(HUD_DB_LINK, HUD_DB_FILE_NAME)
        return get_hud_db()


def get_cfg_db():
    try:
        with open(CFG_DB_FILE_NAME) as f:
            r = reader(f, delimiter=';')
            return [i for i in r]
    except FileNotFoundError:
        print('Downloading hud db...')
        download_file_to_disk(CFG_DB_LINK, CFG_DB_FILE_NAME)
        return get_sound_db()
