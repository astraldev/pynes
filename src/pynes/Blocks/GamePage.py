from __future__ import annotations

from gi.repository import Gtk
from threading import Thread
from time import sleep

from pynes.Managers.GameEngine import GameEngine
from pynes.Blocks.Controls import ControlsBox
from pynes.Managers.GameState import GameState
from pynes.Managers.Preferences import Preferences
from pynes.Blocks.Tile import Tile, TileBox

class GameBox(Gtk.Box):
    def _setup_page(self, engine: GameEngine, *args):
        children = []
        _first_child = self.get_first_child()

        if _first_child is not None:
            children.append(_first_child)
            while _first_child.get_next_sibling():
                _first_child = _first_child.get_next_sibling()
                children.append(_first_child)
        
        for child in children:
            self.remove(child)

        self.engine = engine
        self.tile_box = TileBox(engine)
        self.ctrl_box = ControlsBox(self.tile_box)
        self.ctrl_box.restart_button.connect("clicked", self.on_restart)

        self.tile_box.set_margin_start(10)
        self.tile_box.set_margin_top(10)
        self.tile_box.set_margin_bottom(10)

        self.append(self.tile_box)
        self.append(self.ctrl_box)

    def __init__(self, *args):
        super().__init__(*args, spacing=5)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.dimension = GameState.get_dimension()

    def start(self, *args):
        GameState.reset()
        self.engine.create_arrangement()
        self.ctrl_box.start()
        Thread(target=self._animate).start()

    def _animate(self, *args):
        length_of_tiles = len(GameState.Tiles)
        if not Preferences.AnimationsEnabled:
            GameState.AnimationOver = True
            return

        def _(tile: Tile, nm):
            sleep(0.025)
            tile.set_name(nm)

        # Dont animate larger than 16x16 grids
        if length_of_tiles >= (16*16):
            GameState.AnimationOver = True
            return

        self.tile_box.add_overlay(self.tile_box.game_over_box)
        for tile in GameState.Tiles:
            nm = tile.get_name()
            tile.set_name("tile-shade")
            sleep(0.025)
            Thread(target=_, args=[tile, nm]).start()

        GameState.AnimationOver = True

        self.tile_box.remove_overlay(self.tile_box.game_over_box)

    def on_restart(self, *args):
        self._setup_page()
        self.start()
