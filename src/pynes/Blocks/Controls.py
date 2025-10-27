from __future__ import annotations
from typing import TYPE_CHECKING

from timeutilities import Time
from gi.repository import Gtk, Adw, Gdk, GLib
from ..GameHandler import GameHandler

if TYPE_CHECKING:
    from .Tile import TileBox

class ControlsBox(Gtk.Box):
    def __init__(self, app: Adw.ApplicationWindow, manager: GameHandler, tilebox: TileBox, *args):
        super().__init__(*args, spacing=10)
        self.__application = app

        self.orientation = Gtk.Orientation.VERTICAL
        self.tick_id = None
        self.tilebox = tilebox

        # Time Passed
        # Tiles Opened
        # Flagged

        self.time_label = Gtk.Label()
        self.time_label.set_markup("<b>Time Taken</b>")

        self.s_time_label = Gtk.Label()
        self.s_time = Time(second=1)

        box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box1.append(self.time_label)
        box1.append(self.s_time_label)

        self.tiles_label = Gtk.Label()
        self.tiles_label.set_markup("<b>Tiles Opened</b>")
        self.s_tiles_label = Gtk.Label(label="00 | 00")

        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box2.append(self.tiles_label)
        box2.append(self.s_tiles_label)

        self.flagged_label = Gtk.Label()
        self.flagged_label.set_markup("<b>Flagged</b>")
        self.s_flagged_label = Gtk.Label(label="00 | 00")

        box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box3.append(self.flagged_label)
        box3.append(self.s_flagged_label)

        box4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box4.set_margin_top(5)
        box4.append(box1)
        box4.append(box2)
        box4.append(box3)

        # - Pause
        # - Restart Button
        # - Menu

        button1 = Gtk.Button(label="Pause")
        button2 = Gtk.Button(label="Restart")
        button3 = Gtk.Button(label="Menu")

        button1.set_size_request(140, 50)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_homogeneous(True)

        box.append(button1)
        button1.set_vexpand(True)
        button1.set_hexpand(True)
        button1.set_margin_bottom(2)

        box.append(button2)
        button2.set_vexpand(True)
        button2.set_hexpand(True)
        button2.set_margin_bottom(2)

        box.append(button3)
        button3.set_vexpand(True)
        button3.set_hexpand(True)

        box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_main.append(box4)

        box4.set_vexpand(True)
        box4.set_hexpand(True)

        box_main.append(box)

        box.set_vexpand(False)
        box.set_hexpand(False)

        box_main.set_margin_start(5)
        box_main.set_margin_end(10)
        box_main.set_margin_top(10)
        box_main.set_margin_bottom(10)

        self.append(box_main)
        box_main.set_vexpand(False)
        box_main.set_hexpand(False)

        self.pause_button = button1
        self.restart_button = button2
        self.menu_button = button3

        self.pause_button.connect("clicked", self._btn_pause)
        self.__application.connect("notify::is-active", self.lost_focus)

        self.pause_button.set_sensitive(True)

        self.pause = False
        self.paused_by = ""

    def lost_focus(self, *args):
        paused_by = "window" if not self.pause else "btn"
        if GameHandler.GameOver: return  # noqa: E701
        if paused_by == "btn" and self.pause: return # noqa: E701
        self.paused_by = paused_by

        self.set_paused(ps=not args[0].is_active())

    def _btn_pause(self, *args):
        self.paused_by = "btn"
        self.set_paused(not self.pause)

    def set_paused(self, paused=False):
        if not self.pause or paused:
            self.tilebox.game_over_box.set_name("tile-paused")
            self.tilebox.over_label.set_markup("<b>Game paused.</b>")
            if not self.tilebox.game_over_box.get_parent():
                self.tilebox.add_overlay(self.tilebox.game_over_box)
            self.pause_button.set_label("Continue")
            self.pause = True

        else:
            self.tilebox.game_over_box.set_name("tile-playing")
            self.tilebox.over_label.set_text("")
            if self.tilebox.game_over_box.get_parent():
                self.tilebox.remove_overlay(self.tilebox.game_over_box)
            self.pause_button.set_label("Pause")
            self.pause = False

    def opened_tile(self, tile, *args):
        if GameHandler.GameOver:
            self.pause_button.set_sensitive(False)
            self.restart_button.set_label("Play Again")
            return

        opened_count = len(GameHandler.OpenedTiles)
        opened_display = f"{opened_count:02}"

        self.s_tiles_label.set_text(
            f"{opened_display} | {len(GameHandler.WinningTiles)}"
        )

        self.s_flagged_label.set_text(
            f"{len(GameHandler.FlaggedTiles)} | {len(GameHandler.MineTiles)}"
        )

        return True

    def _right_clicked(self, gesture, *event):
        # Right click event
        if gesture.get_button() == Gdk.BUTTON_SECONDARY:
            gesture.get_widget()._toogle_icon()
            self.s_flagged_label.set_text("{} | {}".format(len(GameHandler.FlaggedTiles), len(GameHandler.MineTiles)))

    def start(self, *args):
        self.s_time_label.set_text("00:00")
        self.s_tiles_label.set_text(
            f"0 | {len(GameHandler.WinningTiles)}"
        )

        self.s_flagged_label.set_text(
            f"0 | {len(GameHandler.MineTiles)}"
        )

        for tile in GameHandler.Tiles:
            tile.connect("toggled", self.opened_tile)
            gesture = Gtk.GestureClick()
            gesture.set_button(Gdk.BUTTON_SECONDARY)
            gesture.connect("pressed", self._right_clicked)
            tile.add_controller(gesture)

        self.tick_id = GLib.timeout_add_seconds(1, self._tick)

    def _tick(self, *args):
        if GameHandler.GameOver:
            return False

        if self.pause or not GameHandler.AnimationOver:
            return True

        self.s_time.tick()
        hour = self.s_time.hour
        mins = self.s_time.minute
        secs = self.s_time.second

        hour_str = f"{hour}:" if hour > 0 else ""
        display_time = f"{hour_str}{mins:02}:{secs:02}"

        self.s_time_label.set_text(display_time)
        GameHandler.CurrentTime = display_time

        return True
