import os

PATH = "/".join(__file__.split("/")[:-1])

MENU_XML = open(f'{PATH}/ui/menu.xml').read()
COLORS   = open(f'{PATH}/ui/colors.css').read()
STYLE    = open(f'{PATH}/ui/style.css').read()
ICON_DIR = f'{PATH}/ui/'
CONFIG_DIR = os.path.expanduser("~/.config/pynes" )
AnimationDir = os.path.join(os.path.expanduser(CONFIG_DIR), "animation")
ANIMATE = False

class ICON:
    FLAGGED = os.path.join(ICON_DIR, 'flagged.png')
    BOMB = os.path.join(ICON_DIR, 'bomb.png')

class CSS_FILES:
    MAIN_COLORS = f'{PATH}/ui/colors.css'
    MAIN = os.path.join(CONFIG_DIR, 'style.css')
    COLORS = os.path.join(CONFIG_DIR, 'colors.css')


## Leaderboard DATA files

LEADERBOARD_FILE = os.path.join(os.path.expanduser(CONFIG_DIR), "leaderboard")
LB_TEXT = "#,User,Tiles,Mines,Time\n"
LB_MAX = 5

## Builder 
