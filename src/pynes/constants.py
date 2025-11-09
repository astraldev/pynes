from . import CONFIG_PATH
from gi.repository import Gtk

import os
import re

class Definitions(object):
    config_path = os.path.join(CONFIG_PATH)

    developer_name = "Ekure Edem"
    developer_email = "ekureedem480@gmail.com"

    app_name = "Pynes"
    description = ""
    copyright = "Copyright © 2021 - 2025 Ekure Edem"
    developer = [f"{developer_name} <{developer_email}>"]
    website = "https://github.com/astraldev/pynes"
    issue_url = "https://github.com/astraldev/pynes/issues/new"
    license = Gtk.License.GPL_3_0

PATH = "/".join(__file__.split("/")[:-1])

MENU_XML = open(f'{PATH}/ui/menu.xml').read()
COLORS   = open(f'{PATH}/ui/colors.css').read()
STYLE    = open(f'{PATH}/ui/style.css').read()
ICON_DIR = f'{PATH}/ui/'
CONFIG_DIR = os.path.expanduser(CONFIG_PATH)
AnimationDir = os.path.join(os.path.expanduser(CONFIG_DIR), "animation")

_re_results = re.findall(r'\d', open(AnimationDir).read())
ANIMATE = True if len(_re_results) > 0 and int(_re_results[0]) == 1 else False

class ICON:
    FLAGGED = os.path.join(ICON_DIR, 'flagged.svg')
    UNSURE = os.path.join(ICON_DIR, 'flagged-unsure.svg')
    BOMB = os.path.join(ICON_DIR, 'bomb.svg')

class CSS_FILES:
    MAIN_COLORS = f'{PATH}/ui/colors.css'
    MAIN = os.path.join(CONFIG_DIR, 'style.css')
    COLORS = os.path.join(CONFIG_DIR, 'colors.css')

