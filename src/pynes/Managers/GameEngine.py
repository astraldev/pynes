from random import choice
from pynes.Blocks.Tile import Tile, TileBox
from pynes.Managers.GameState import GameState


class GameEngine:
    """Handles game logic and mechanics"""

    def __init__(self, tilebox: TileBox, *args):
        self.tile_box = tilebox

    def game_play(self, *args):
        """Override in subclass to handle game start"""
        pass

    def game_option_8x8(self, *args):
        """Set game to 8x8 grid with 15% mines"""
        GameState.set_dimension(8, 8, 15)
        self.game_play()

    def game_option_16x16(self, *args):
        """Set game to 16x16 grid with 15% mines"""
        GameState.set_dimension(16, 16, 15)
        self.game_play()

    def game_option_24x16(self, *args):
        """Set game to 24x16 grid with 15% mines"""
        GameState.set_dimension(24, 16, 15)
        self.game_play()

    def game_option_custom(self, *args):
        """Set custom game dimensions"""
        row = int(args[1].get_value())
        col = int(args[2].get_value())
        mine = int(args[3].get_value())
        GameState.set_dimension(row, col, mine)
        self.game_play()

    def _put_mines(self, area: list[int], num: int) -> list[int]:
        """Randomly place mines on the board"""
        results = []
        i = 0

        while i < num:
            chosen = choice(area)
            if chosen not in results:
                results.append(chosen)
                i += 1
            if i == num:
                break

        GameState.MineTiles = results
        return results

    def _get_tile(self, location: int, dx: int, dy: int) -> Tile | None:
        """Get a neighboring tile at relative position (dx, dy)"""
        row_len, col_len = GameState.game_dimension[:2]
        row, col = divmod(location, row_len)
        new_row, new_col = row + dx, col + dy
        
        if 0 <= new_row < col_len and 0 <= new_col < row_len:
            return GameState.Tiles[new_row * row_len + new_col]
        return None

    def get_top_tile(self, location: int) -> Tile | None:
        return self._get_tile(location, -1, 0)

    def get_bottom_tile(self, location: int) -> Tile | None:
        return self._get_tile(location, 1, 0)

    def get_left_tile(self, location: int) -> Tile | None:
        return self._get_tile(location, 0, -1)

    def get_right_tile(self, location: int) -> Tile | None:
        return self._get_tile(location, 0, 1)

    def get_top_left_tile(self, location: int) -> Tile | None:
        return self._get_tile(location, -1, -1)

    def get_top_right_tile(self, location: int) -> Tile | None:
        return self._get_tile(location, -1, 1)

    def get_bottom_left_tile(self, location: int) -> Tile | None:
        return self._get_tile(location, 1, -1)

    def get_bottom_right_tile(self, location: int) -> Tile | None:
        return self._get_tile(location, 1, 1)

    # TODO: Review logic here
    def _set_up_game(self, area: list, m_locations: list[int]) -> list:
        """Set up the game board with mine counts"""
        # Initialize all positions to 0
        for index in range(len(area)):
            area[index] = 0

        mx = len(area)

        # Calculate mine counts for each position
        for location in m_locations:
            # Get all 8 neighbors
            neighbors = [
                self.get_left_tile(location),
                self.get_right_tile(location),
                self.get_top_tile(location),
                self.get_bottom_tile(location),
                self.get_top_right_tile(location),
                self.get_top_left_tile(location),
                self.get_bottom_right_tile(location),
                self.get_bottom_left_tile(location),
            ]

            # Increment count for each valid neighbor
            for neighbor in neighbors:
                if neighbor is not None:
                    neighbor_pos = neighbor.position
                    if 0 <= neighbor_pos < mx:
                        area[neighbor_pos] += 1

        # Mark mine positions and winning tiles
        for location in m_locations:
            area[location] = "m"

        for index, item in enumerate(area):
            if area[index] == 0:
                area[index] = ""
            if area[index] != "m":
                GameState.WinningTiles.append(index)

        return area

    def create_arrangement(self):
        """Create the game board arrangement"""
        rows, cols, mine_percent = GameState.game_dimension
        total = rows * cols
        total_array = list(range(total))

        num_of_mines = int(round(total * (mine_percent / 100) * 1.041666667))
        mine_locations = self._put_mines(total_array.copy(), num_of_mines)
        total_array = self._set_up_game(total_array, mine_locations)

        self.tile_box.set_dimensions()
        
        for index, tile_type in enumerate(total_array):
            mine = tile_type == "m"
            lab = "" if mine else tile_type
            tile_type_val = 0 if tile_type == "" else 2 if mine else 1
            tile = Tile(self, index, tile_type_val, lab)
            self.tile_box.add_tile(tile)
            GameState.Tiles.append(tile)