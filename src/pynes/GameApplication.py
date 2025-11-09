from pynes.GameWindow import GameWindow
from pynes.Popups.Leaderboard import LeaderBoardWindow
from pynes.Popups.PreferenceDialog import PreferenceDialog
from pynes.Popups.About import AboutPynes
from gi.repository import Gtk, Gio

class Game(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.astralco.pyne", **kwargs)
        self.window = None
        self.about = AboutPynes.create()
        self.preferences = PreferenceDialog()

    def show_about_window(self, *args):
        self.about.present()
    
    def show_preference_window(self, *args):
        self.preferences.present()

    def show_leaderboard_window(self, *args):
        leaderboard = LeaderBoardWindow()
        leaderboard.present()

    def do_startup(self, *args):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about_window)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)

        action.connect("activate", self.on_quit)
        self.add_action(action)
        self.set_accels_for_action('app.quit', ["<Ctrl>Q"])

        action = Gio.SimpleAction.new("leaderboard", None)
        action.connect("activate", self.show_leaderboard_window)
        self.add_action(action)
        self.set_accels_for_action('app.leaderboard', ['<Ctrl>L'])

        action = Gio.SimpleAction.new("preferences", None)
        action.connect("activate", self.show_preference_window)
        self.set_accels_for_action('app.preferences', ['<Ctrl>P'])
        self.add_action(action)

    # Windows are associated with the application
    # when the last one is closed the application shuts down
    def do_activate(self, *args):
        if not self.window:
            self.window = GameWindow(application=self)
            self.window.connect("destroy", self.on_quit)
            self.window.set_icon_name("pynes")
            self.add_window(self.window)
        self.window.present()

    def on_quit(self, *args):
        self.quit()
