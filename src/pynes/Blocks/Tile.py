from __future__ import annotations
from typing import TYPE_CHECKING
from random import randint
from enum import Enum
from gi.repository import Gtk, GLib

from ..constants import ICON

if TYPE_CHECKING:
    from pynes.GameHandler import GameHandler

class TileType(Enum):
    Plain = 0
    Numbered = 1
    Bomb = 2

class TileState(Enum):
    Unset = 0
    Flagged = 1
    Unsure = 2

class Tile(Gtk.ToggleButton):
    # The icons should match the tile states
    icons = [None, "flag", "question"]
    
    @staticmethod
    def dummy(state=True ,mine=False, flag=False, question=False, is_active=False):
        tl = Tile(0, mine, (2 if mine else 1), randint(0, 4))
        tl.dummy = True
        tl.active_dummy = is_active
        tl.set_size_request(32, 32)
        tl.set_vexpand(True)
        tl.set_margin_end(2)
        tl.set_margin_start(2)
        tl.set_margin_bottom(2)
        tl.set_margin_top(2)
        tl.set_hexpand(True)

        if mine:
            tl.set_name("mine")
            b_icon = Gtk.Image.new_from_file(ICON.BOMB)
            b_icon.set_icon_size(Gtk.IconSize.NORMAL)
            tl.set_child(b_icon)
            
        if flag:
            tl._toogle_icon()
            
        if question:
            tl._toogle_icon()
            tl._toogle_icon()
            
        if state and not (question or flag or mine or is_active):
            tl.set_name("tile-on")
            tl.set_label(str(tl.lab))
            tl.set_active(state)
            tl.toggled = True
        
        def _toggle(tile:Tile, *args):
            if tile.toggled and not tile.icon_position > 1:
                tl.set_name("tile")
                tl.set_label("")
                tl.set_active(False)
                tl.toggled = False
                
            elif not tile.icon_position > 1:
                tl.set_name("tile-on")
                tl.set_label(str(tl.lab))
                tl.set_active(state)
                tl.toggled = True
        
        if is_active:
            tl.connect("clicked", _toggle)
        
        return tl

    def __init__(self, manager: GameHandler, position: int, tile_type: TileType, label: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_state = TileState.Unset
        self.__game_manager = manager

        self.connect("toggled", self.clicked)
        self.connect("clicked", self.clicked)
        self.set_size_request(24, 24)
        self.position = position
        self.active_dummy = False
        self.label = label
        self.type = tile_type
        self.toggled = False
        self.dummy = False
        self.set_name("tile")

    def clicked(self, *args):
        return True
    
    def get_next_state(self, state: TileState):
        return {
            [TileState.Unset]: TileState.Flagged,
            [TileState.Flagged]: TileState.Unsure,
            [TileState.Unsure]: TileState.Unset,
        }[state]

    def _toogle_icon(self, *args):
        if self.toggled: return  # noqa: E701

        next_state = self.get_next_state(self.current_state)

        if next_state is TileState.Flagged:
            img = Gtk.Image.new_from_file(ICON.FLAGGED)
            img.set_icon_size(Gtk.IconSize.NORMAL)

            self.set_child(img)
            self.set_name("tile-flagged")
            self.__game_manager.FlaggedTiles.append(self)
        
        elif next_state is TileState.Unsure:
            img = Gtk.Image.new_from_file(ICON.UNSURE)
            self.set_child(img)
            img.set_icon_size(Gtk.IconSize.NORMAL)
            self.set_name("tile-flagged-u")

        elif next_state is TileState.Unset:
            self.set_child(None)
            self.set_name("tile")

            if self in self.__game_manager.FlaggedTiles:
                self.__game_manager.FlaggedTiles.remove(self)

        self.current_state = next_state

class TileBox(Gtk.Overlay):
    def __init__(self, manager: GameHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__game_manager = manager
        self.next_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.main_box)

        # row | col
        self.flow = Gtk.Grid()

        self.next_box.append(self.flow)
        self.main_box.append(self.next_box)
        self.dimensions = self.__game_manager.get_game_dimension()

        self.start = 0
        self.next = 0

        self.game_over_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.over_label = Gtk.Label()
        self.over_label.set_name("tile-label")

        self.over_label.set_valign(Gtk.Align.CENTER)
        self.over_label.set_halign(Gtk.Align.CENTER)
        self.over_label.set_vexpand(True)
        self.over_label.set_hexpand(True)

        self.game_over_box.append(self.over_label)
        self.game_over_box.set_name("tile-playing")
    
    def _is_game_over(self):
        return self.__game_manager.is_game_over
    
    def show_game_over_overlay(self):
        self.game_over_box.set_name("tile-failed")
        self.over_label.set_text("A mine exploded.")

        if not self.game_over_box.get_parent():
            self.add_overlay(self.game_over_box)

    def show_game_won_overlay(self):
        self.game_over_box.set_name("tile-won")
        self.over_label.set_text("You won !!")

        if not self.game_over_box.get_parent():
            self.add_overlay(self.game_over_box)

    def set_dimensions(self, *args):
        self.dimensions = self.__game_manager.get_game_dimension()
        # self.flow.set_min_children_per_line(self.dimensions[0])
        # self.flow.set_max_children_per_line(self.dimensions[0])

    # alias -> check_mine
    def open_tile(self, tile: Tile, *event):
        game_is_over = self._is_game_over()

        # Do not open a flagged tile
        if tile.current_state is not TileState.Unset \
            or tile.toggled or game_is_over:
            return True
        
        # Set the on class to the tile that's not a bomb
        if tile.current_state is TileState.Unset and tile.type is not TileType.Bomb:
            tile.set_name("tile-on")

        location = tile.position
        tile.toggled = True

        t_r = self.get_right_tile(location)
        t_l = self.get_left_tile(location)
        t_top = self.get_top_tile(location)
        t_top_r = self.get_bottom_right_tile(location)
        t_top_l = self.get_top_left_tile(location)
        t_bottom = self.get_bottom_tile(location)
        t_bottom_r = self.get_bottom_right_tile(location)
        t_bottom_l = self.get_bottom_left_tile(location)

        # Check if tile is empty
        if tile.type == TileType.Plain and not game_is_over:
            GLib.idle_add(self._open_tiles, [t_r, t_top_r])
            GLib.idle_add(self._open_tiles, [t_bottom_r, t_l])
            GLib.idle_add(self._open_tiles, [t_top_l, t_bottom_l])
            GLib.idle_add(self._open_tiles, [t_top, t_bottom])

        if tile.type == TileType.Numbered:
            tile.set_label(str(tile.label))

        GameHandler.OpenedTiles.append(location)

        if tile.type == TileType.Bomb:
            self.__game_manager.end_game()
            self._open_tiles(GameHandler.Tiles, True)
            self.show_game_over_overlay()

        opened = list(sorted(GameHandler.OpenedTiles))
        winning = list(sorted(GameHandler.WinningTiles))

        if (opened == winning) and not game_is_over:
            self.__game_manager.end_game()
            self._open_tiles(GameHandler.Tiles, True)
            self.show_game_won_overlay()
            self._show_leaderboard(self._add_score_to_leaderboard())

        return True

    def _open_tiles(self, tiles: list[Tile], all=False):
        used_tiles = [tile for tile in tiles if tile is not None]
        for tile in used_tiles:
            if self._is_game_over():
                if (tile.current_state is not TileState.Unset) and (tile.type is not TileType.Bomb):
                    tile.set_name("tile-flagged-x")
                    tile.set_child(None)
                    tile.set_label(str(tile.label))

            if tile.current_state is not TileState.Unset:
                continue

            if all and tile.type is TileType.Bomb:
                b_icon = Gtk.Image.new_from_file(ICON.BOMB)
                b_icon.set_icon_size(Gtk.IconSize.NORMAL)

                tile.set_name("mine")
                tile.set_child(b_icon)
                tile.set_active(False)

            if tile.type is TileType.Numbered or tile.type is TileType.Plain:
                tile.set_active(True)

    def add_tile(self, tile):
        self.flow.attach(tile, self.start, self.next, 1, 1)
        tile.set_vexpand(True)
        tile.set_margin_end(2)
        tile.set_margin_start(2)
        tile.set_margin_bottom(2)
        tile.set_margin_top(2)
        tile.set_hexpand(True)

        self.start += 1
        if self.start == GameHandler.game_dimension[0]:
            self.start = 0
            self.next += 1

        tile.connect("toggled", self.open_tile)

        w, h = GameHandler.game_dimension[0]*24, GameHandler.game_dimension[1]*24
        self.set_size_request(w, h)
