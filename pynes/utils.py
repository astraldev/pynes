
import os
from pynes.constants import COLORS, CONFIG_DIR, STYLE, LEADERBOARD_FILE, LB_TEXT, AnimationDir

def setup_css_file(force=False):
    fn =  os.path.join(CONFIG_DIR, "style.css")
    fn2 = os.path.join(CONFIG_DIR, "colors.css")
    fn3 = os.path.join(CONFIG_DIR, "colors.backup.css")
    
    if os.path.isfile(os.path.expanduser(fn3)) and os.path.isfile(os.path.expanduser(fn2)):
        fn2 = fn3
    if (not (os.path.isfile(os.path.expanduser(fn2)) and os.path.isfile(os.path.expanduser(fn)))):
        with open(os.path.expanduser(fn2), "w") as fd:
            fd.write(COLORS)
        with open(os.path.expanduser(fn), "w") as fd:
            fd.write(STYLE)
    return os.path.expanduser(fn), os.path.expanduser(fn2),

def check_config():
    global ANIMATE
    if not os.path.isdir(os.path.expanduser(CONFIG_DIR)):
        os.mkdir(os.path.expanduser(CONFIG_DIR))

    if not os.path.exists(LEADERBOARD_FILE):
        open(LEADERBOARD_FILE, "w").write(LB_TEXT)
    
    if not os.path.exists(AnimationDir):
        open(AnimationDir, "w").write("True")
    elif open(AnimationDir, "r").read() != "True" or open(AnimationDir, "r").read() != "False":
        open(AnimationDir, "w").write("True")
    else:
        ANIMATE = open(AnimationDir).read()
