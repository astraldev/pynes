import csv
from io import StringIO
from random import choice
from timeutilities import Time

from pynes.Blocks.Tile import Tile
from pynes.constants import LB_TEXT, LEADERBOARD_FILE

class GameHandler:
    game_dimension = [0, 0, 0]
    AnimationOver = False
    Tiles: list[Tile] = []
    WinningTiles: list[Tile] = []
    OpenedTiles: list[Tile] = []
    Menu = None
    MainWindow = None
    MineTiles = []
    FlaggedTiles = []
    CurrentTime = "00:00"
    GameOver = False

    def __init__(self, *args):
        GameHandler.game_dimension = [0, 0, 0]
        GameHandler.GameOver = False

    def end_game(self):
        GameHandler.GameOver = True

    def game_play(self, *args): pass

    def game_option_8x8(self, *args):
        GameHandler.game_dimension = [8, 8, 15]
        self.game_play()

    def game_option_16x16(self, *args):
        GameHandler.game_dimension = [16, 16, 15]
        self.game_play()

    def game_option_24x16(self, *args):
        GameHandler.game_dimension = [24, 16, 15]
        self.game_play()

    def game_option_custom(self, *args):
        row = int(args[1].get_value())
        col = int(args[2].get_value())
        mine = int(args[3].get_value())
        GameHandler.game_dimension = [row, col, mine]
        self.game_play()

    def get_game_dimension(self, *args):
        return GameHandler.game_dimension

    def _put_mines(self, area, num):
        results = []
        i = 0

        while i < num:
            choosen = choice(area)
            if choosen not in results:
                results.append(choosen)
                i += 1
            if i == num:
                break

        GameHandler.MineTiles = results
        return results
    
    def _arrange_scores(self, data, *args):
        targets = {}

        reader = csv.reader(StringIO(data))
        rows = list(reader)

        for row in rows:
            try:
                _, __, num, mines, time_str = row

                mines = int(mines) or 1
                num = int(num) or 1

                parts = time_str.split(":")
                time_sec = int(parts[-1])
                time_min = int(parts[-2])
                time_hour = int(parts[-3]) if len(parts) > 2 else 0

                total_seconds = Time(time_sec, time_min, time_hour).to_seconds()
                res_tar = round(total_seconds / (mines * num), 8)
                targets[str(res_tar)] = row
            except Exception:
                continue

        targets_sorted = dict(sorted(targets.items(), key=lambda x: float(x[0])))
        last_key = next((k for k, v in targets.items() if v == rows[-1]), None)

        output = []
        last_index = None

        for index, (key, row) in enumerate(targets_sorted.items(), 1):
            row[0] = str(index)
            output.append(",".join(map(str, row)))
            if key == last_key:
                last_index = index

        return output, last_index

    def _organize_config(self, *args):
        file = list(open(LEADERBOARD_FILE, "r"))
        heading = file[0] or LB_TEXT
        data = "\n".join(file[1:])

        sorted_content, loc = self._arrange_scores(data)
        output = [heading, *sorted_content]

        open(LEADERBOARD_FILE, "w").write("\n".join(output))
        return loc

    # Top
    def get_top_tile(self, location):
        position = location - GameHandler.game_dimension[0]
        if position >= 0:
            return GameHandler.Tiles[position]

    # Bottom
    def get_bottom_tile(self, location):
        mx = len(GameHandler.Tiles)
        position = location + GameHandler.game_dimension[0]
        if (position < mx):
            return GameHandler.Tiles[position]

    # Right
    def get_right_tile(self, location):
        mx = len(GameHandler.Tiles)

        # Positions to avoid
        avoid = [GameHandler.game_dimension[0]]
        position = location + 1

        for x in range(GameHandler.game_dimension[1]):
            avoid.append(avoid[x] + GameHandler.game_dimension[0])

        if (position not in avoid) and position < mx:
            return GameHandler.Tiles[position]

    # Left
    def get_left_tile(self, location):
        avoid = [-1]
        position = location - 1

        for x in range(GameHandler.game_dimension[1]):
            avoid.append(avoid[x]+GameHandler.game_dimension[0])

        if (position not in avoid) and position >= 0:
            return GameHandler.Tiles[position]

    # Top Left
    def get_top_left_tile(self, location):
        avoid = [0]
        avoid_right = [GameHandler.game_dimension[0]+1]
        position = location - GameHandler.game_dimension[0] - 1

        for x in range(GameHandler.game_dimension[1]):
            avoid.append(avoid[x] + GameHandler.game_dimension[0])

        for x in range(GameHandler.game_dimension[1]):
            avoid_right.append(avoid[x] + GameHandler.game_dimension[0])

        if location in avoid_right:
            return

        if position >= 0 and position not in avoid:
            return GameHandler.Tiles[position]

    # Bottom Left
    def get_bottom_left_tile(self, location):
        avoid = [-1]
        avoid_right = [GameHandler.game_dimension[0]+1]
        mx = len(GameHandler.Tiles)
        position = location + GameHandler.game_dimension[0] - 1

        for x in range(GameHandler.game_dimension[1]):
            avoid.append(avoid[x]+GameHandler.game_dimension[0])

        for x in range(GameHandler.game_dimension[1]):
            avoid_right.append(avoid[x]+GameHandler.game_dimension[0])

        if location in avoid_right:
            return

        if position < mx and (position) not in avoid:
            return GameHandler.Tiles[position]

    # Top Right
    def get_top_right_tile(self, location):
        avoid_left = [-1]
        avoid = [GameHandler.game_dimension[0]]
        position = location - GameHandler.game_dimension[0] + 1

        for x in range(GameHandler.game_dimension[1]):
            avoid.append(avoid[x]+GameHandler.game_dimension[0])

        for x in range(GameHandler.game_dimension[1]):
            avoid_left.append(avoid[x]+GameHandler.game_dimension[0])

        if location in avoid_left:
            return

        if position >= 0 and position not in avoid:
            return GameHandler.Tiles[position]

    # Bottom Right
    def get_bottom_right_tile(self, location):
        avoid_left = [-1]
        avoid = [GameHandler.game_dimension[0]]
        position = location + GameHandler.game_dimension[0] + 1
        mx = len(GameHandler.Tiles)

        for x in range(GameHandler.game_dimension[1]):
            avoid.append(avoid[x]+GameHandler.game_dimension[0])

        for x in range(GameHandler.game_dimension[1]):
            avoid_left.append(avoid[x]+GameHandler.game_dimension[0])

        if location in avoid_left:
            return

        if location in avoid:
            return GameHandler.Tiles[location]

        if position < mx and position not in avoid:
            return GameHandler.Tiles[position]

    def _set_up_game(self, area, m_locations):
        for index, item in enumerate(area):
            area[index] = 0

        avoid_right = [GameHandler.game_dimension[0]]
        for x in range(GameHandler.game_dimension[1]):
            avoid_right.append(avoid_right[x]+GameHandler.game_dimension[0])

        avoid_left = [-1]
        for x in range(GameHandler.game_dimension[1]):
            avoid_left.append(avoid_left[x]+GameHandler.game_dimension[0])

        mx = len(area)

        for location in m_locations:
            if ((location-1) not in avoid_left) and (location-1) > 0:  # Left
                area[location-1] += 1
            if ((location+1) not in avoid_right) and (location+1) < mx:  # Right
                area[location+1] += 1
            # Top
            if (location-GameHandler.game_dimension[0] > -1):
                area[location-GameHandler.game_dimension[0]] += 1
            # Bottom
            if (location+GameHandler.game_dimension[0] < mx):
                area[location+GameHandler.game_dimension[0]] += 1
            # Top Right
            if (location-GameHandler.game_dimension[0]+1) > 0 and (location-GameHandler.game_dimension[0]+1) not in avoid_right:
                area[location-GameHandler.game_dimension[0]+1] += 1
            # Top Left
            if (location-GameHandler.game_dimension[0]-1) > 0 and (location-GameHandler.game_dimension[0]-1) not in avoid_left:
                area[location-GameHandler.game_dimension[0]-1] += 1
            # Bottom Right
            if (location+GameHandler.game_dimension[0]+1) < mx and (location+GameHandler.game_dimension[0]+1) not in avoid_right:
                area[location+GameHandler.game_dimension[0]+1] += 1
            # Bottom Left
            if (location+GameHandler.game_dimension[0]-1) < mx and (location+GameHandler.game_dimension[0]-1) not in avoid_left:
                area[location+GameHandler.game_dimension[0]-1] += 1
        for location in m_locations:
            area[location] = "m"
        for index, item in enumerate(area):
            if area[index] == 0:
                area[index] = ""
            if area[index] != "m":
                GameHandler.WinningTiles.append(index)

        return area

    def create_arrangement(self, *args):
        total = GameHandler.game_dimension[0] * GameHandler.game_dimension[1]
        total_array = list(range(total))
        mine_array = total_array

        # lol -- magic number multiplication
        num_of_mines = int(round(total * (GameHandler.game_dimension[2] / 100) * 1.041666667, 0))
        location_of_mines = self._put_mines(mine_array, num_of_mines)
        total_array = self._set_up_game(total_array, location_of_mines)
        self.tile_box.set_dimensions()

        for index, tile_type in enumerate(total_array):
            mine = (tile_type == "m")
            # 0 = empty
            # 1 = Number
            # 2 = Mine
            lab = tile_type

            if tile_type == "":
                tile_type = 0
            elif isinstance(tile_type, int):
                tile_type = 1
            elif tile_type == "m":
                tile_type = 2
                lab = ""

            tile = Tile(index, mine, tile_type, lab)
            self.tile_box.add_tile(tile)
            GameHandler.Tiles.append(tile)

