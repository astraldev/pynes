from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pynes.Blocks.Tile import Tile

class GameState:
    """Manages the global state of the game"""
    
    # [rows, cols, mine_percentage]
    game_dimension = [0, 0, 0]

    AnimationOver = False
    Tiles: list[Tile] = []
    WinningTiles: list[int] = []
    OpenedTiles: list[int] = []
    Menu = None
    MainWindow = None
    MineTiles: list[int] = []
    FlaggedTiles: list[Tile] = []
    CurrentTime = "00:00"
    GameOver = False

    @classmethod
    def reset(cls):
        """Reset all game state variables"""
        cls.Tiles = []
        cls.WinningTiles = []
        cls.OpenedTiles = []
        cls.MineTiles = []
        cls.FlaggedTiles = []
        cls.AnimationOver = False
        cls.CurrentTime = "00:00"
        cls.GameOver = False

    @classmethod
    def set_dimension(cls, rows: int, cols: int, mine_percent: int):
        """Set the game dimension"""
        cls.game_dimension = [rows, cols, mine_percent]

    @classmethod
    def get_dimension(cls) -> list[int]:
        """Get the current game dimension"""
        return cls.game_dimension

    @classmethod
    def end_game(cls):
        """Mark the game as over"""
        cls.GameOver = True

    @classmethod
    def is_game_won(cls) -> bool:
        """Check if the game is won"""
        opened = sorted(cls.OpenedTiles)
        winning = sorted(cls.WinningTiles)
        return opened == winning and not cls.GameOver

    @classmethod
    def add_opened_tile(cls, position: int):
        """Add a tile position to opened tiles"""
        if position not in cls.OpenedTiles:
            cls.OpenedTiles.append(position)

    @classmethod
    def add_flagged_tile(cls, tile: Tile):
        """Add a tile to flagged tiles"""
        if tile not in cls.FlaggedTiles:
            cls.FlaggedTiles.append(tile)

    @classmethod
    def remove_flagged_tile(cls, tile: Tile):
        """Remove a tile from flagged tiles"""
        if tile in cls.FlaggedTiles:
            cls.FlaggedTiles.remove(tile)