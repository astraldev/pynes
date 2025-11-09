import os
import csv

from gi.repository import Adw, Gtk
from timeutilities import Time
from pynes.Managers.GameState import GameState
from pynes.Managers.FileManager import FileManager

LEADERBOARD_FILE = FileManager.LEADERBOARD_FILE
LB_TEXT = "#,User,Tiles,Mines,Time\n"

class LeaderBoardWindow(Adw.Window):
    def __init__(self, loc: int, *args):
        super().__init__(*args)
        self.set_title("Leaderboard")
        self.set_default_size(400, 500)
        self.set_modal(True)
        self.set_resizable(False)

        # Toolbar + Content view
        view = Adw.ToolbarView()
        header = Adw.HeaderBar()
        self.reset_button = Gtk.Button(label="Reset")
        self.reset_button.add_css_class("destructive-action")
        header.pack_start(self.reset_button)
        view.add_top_bar(header)

        self.reader = list(csv.reader(FileManager.read_text(LEADERBOARD_FILE)))
        self.location = loc

        # Store and TreeView
        self.store = Gtk.ListStore(str, str, str, str, str)
        self._fill_store()
        self.treeview = Gtk.TreeView(model=self.store)
        self._fill_columns()

        scroll = Gtk.ScrolledWindow()
        scroll.set_child(self.treeview)
        scroll.set_vexpand(True)
        scroll.set_hexpand(True)
        view.set_content(scroll)

        self.set_content(view)
        self.reset_button.connect("clicked", self._on_reset)
        self.present()

    def _get_titles(self):
        return self.reader[0]

    def _get_content(self):
        return self.reader[1:]

    def _fill_store(self):
        for ind, items in enumerate(self._get_content(), 0):
            if self.location == ind:
                self.location = self.store.append()
                self.store.insert_with_values(ind, (0, 1, 2, 3, 4), items)
                continue
            self.store.insert_with_values(ind, (0, 1, 2, 3, 4), items)

    def _fill_columns(self):
        for index, title in enumerate(self._get_titles()):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=index)
            self.treeview.append_column(column)
        model = self.treeview.get_model()
        self.treeview.show()
        if self.location is not None and not isinstance(self.location, int):
            loc = model.get_path(self.location)
            if loc is not None:
                self.treeview.set_cursor(loc)
    
    def hydrate_list_view(self):
        """Read the current leaderboard file then refresh the list view"""
        self.store.clear()
        self.reader = list(csv.reader(FileManager.read_text(LEADERBOARD_FILE)))
        self._fill_store()
    
    @staticmethod
    def update_score():
        name = os.environ.get("USER", "Unknown")
        specs = f"{len(GameState.Tiles)},{len(GameState.MineTiles)}"
        time = GameState.CurrentTime
        lines = list(FileManager.read_text(LEADERBOARD_FILE))[1:]
        line = f"{len(lines)},{name},{specs},{time}\n"

        def _extract_time(data: str):
            time = data.split(",")[3]
            hrs, mins, secs = time.split(":")
            hrs, mins, secs = int(hrs), int(mins), int(secs)
            return Time(secs, mins, hrs).to_seconds()

        lines.append(line)
        lines.sort(_extract_time)
        FileManager.write_text(LEADERBOARD_FILE, "\n".join([LB_TEXT, *lines]))

    def _on_reset(self, *args):
        FileManager.write_text(LEADERBOARD_FILE, LB_TEXT)
        self.hydrate_list_view()

