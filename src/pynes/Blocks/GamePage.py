from __future__ import annotations

from gi.repository import Gtk
from threading import Thread
from time import sleep

from pynes.Blocks.Controls import ControlsBox
from pynes.Preferences import Preferences
from pynes.GameHandler import GameHandler
from pynes.Blocks.Tile import Tile, TileBox

class GameBox(Gtk.Box):
    def _setup_page(self, manager: GameHandler, *args):
        children = []
        _first_child = self.get_first_child()

        if _first_child is not None:
            children.append(_first_child)
            while _first_child.get_next_sibling():
                _first_child = _first_child.get_next_sibling()
                children.append(_first_child)
        
        for child in children:
            self.remove(child)

        self.manager = manager
        self.tile_box = TileBox(manager)
        self.opt = ControlsBox(self.tile_box)
        self.opt.restart_button.connect("clicked", self.on_restart)

        self.tile_box.set_margin_start(10)
        self.tile_box.set_margin_top(10)
        self.tile_box.set_margin_bottom(10)

        self.append(self.tile_box)
        self.append(self.opt)

    def __init__(self, *args):
        super().__init__(*args, spacing=5)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.dimension = self.manager.get_game_dimension()

    def start(self, *args):
        GameHandler.Tiles = []
        GameHandler.WinningTiles = []
        GameHandler.OpenedTiles = []
        GameHandler.GameOver = False
        GameHandler.MineTiles = []
        GameHandler.FlaggedTiles = []
        GameHandler.AnimationOver = False
        GameHandler.CurrentTime = ""

        self.manager.create_arrangement()
        self.opt.start()
        self.opt.menu_button.connect("clicked", GameHandler.Menu)
        Thread(target=self._animate).start()

    def _animate(self, *args):
        length_of_tiles = len(GameHandler.Tiles)
        if not Preferences.AnimationsEnabled:
            GameHandler.AnimationOver = True
            return

        def _(tile: Tile, nm):
            sleep(0.025)
            tile.set_name(nm)

        # Dont animate larger than 16x16 grids
        if length_of_tiles >= (16*16):
            GameHandler.AnimationOver = True
            return

        self.tile_box.add_overlay(self.tile_box.game_over_box)
        for tile in GameHandler.Tiles:
            nm = tile.get_name()
            tile.set_name("tile-shade")
            sleep(0.025)
            Thread(target=_, args=[tile, nm]).start()

        GameHandler.AnimationOver = True

        self.tile_box.remove_overlay(self.tile_box.game_over_box)

    def on_restart(self, *args):
        self._setup_page()
        self.start()
