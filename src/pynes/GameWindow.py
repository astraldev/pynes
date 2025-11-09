from gi.repository import Gtk

from pynes.Blocks.GamePage import GameBox
from pynes.GameHandler import GameHandler
from pynes.constants import MENU_XML

class GameWindow(Gtk.ApplicationWindow):
    def __init__(self, handler: GameHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        GameHandler.MainWindow = self
        self.__handler = handler

        self.header_bar = Gtk.HeaderBar()
        self.set_title("pynes")
        self.header_bar.set_show_title_buttons(True)
        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        menu = builder.get_object("app-menu")

        button = Gtk.MenuButton.new()

        button.set_direction(Gtk.ArrowType.NONE)
        popover = Gtk.PopoverMenu.new_from_model(menu)
        button.set_popover(popover)

        self.set_titlebar(self.header_bar)
        self.header_bar.pack_start(button)
        self.set_default_size(570, 470)

        self.stack = Gtk.Stack()
        self.set_child(self.stack)

        self._init_option_menu()
        self._init_game_stack()
    

    def update_subtitle(self, x = None):
        self.set_title(f"pynes - {x}" if x else " pynes ")

    def _init_option_menu(self):
        self.option = Gtk.Stack()
        grid = Gtk.FlowBox()
        grid.set_max_children_per_line(2)
        grid.set_min_children_per_line(2)
        grid.set_selection_mode(Gtk.SelectionMode.NONE)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box_inner.append(grid)
        grid.set_vexpand(True)
        grid.set_hexpand(True)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_halign(Gtk.Align.CENTER)
        box.append(box_inner)
        self.option.add_named(box, "main")

        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box2_inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        grid2 = Gtk.Grid()
        grid2.set_column_homogeneous(True)
        grid2.set_row_homogeneous(True)

        # grid items
        row_label, col_label, mine_label = Gtk.Label(label="Rows"), Gtk.Label(label="Columns"), Gtk.Label(label="Mine ( % )")
        row_spin, col_spin, mine_spin = Gtk.SpinButton(), Gtk.SpinButton(), Gtk.SpinButton()

        row_spin.set_adjustment(Gtk.Adjustment(upper=32, value=24, lower=3, step_increment=1, page_increment=5))
        col_spin.set_adjustment(Gtk.Adjustment(upper=22, value=16, lower=3, step_increment=1, page_increment=5))
        mine_spin.set_adjustment(Gtk.Adjustment(upper=90, value=15, lower=1, step_increment=1, page_increment=5))

        grid2.attach(row_label, 0, 0, 1, 1)
        grid2.attach(row_spin, 1, 0, 1, 1)
        grid2.attach(col_label, 0, 1, 1, 1)
        grid2.attach(col_spin, 1, 1, 1, 1)
        grid2.attach(mine_label, 0, 2, 1, 1)
        grid2.attach(mine_spin, 1, 2, 1, 1)

        play_btn = Gtk.Button(label="Go")
        play_btn.connect("clicked", self.__handler.game_option_custom, row_spin, col_spin, mine_spin)
        back_btn = Gtk.Button(label="Back")
        back_btn.connect("clicked", self._from_custom)

        grid2.attach(play_btn, 1, 3, 1, 1)
        grid2.attach(back_btn, 0, 3, 1, 1)
        grid2.set_column_spacing(2)
        grid2.set_row_spacing(2)

        box2_inner.append(grid2)
        box2.append(box2_inner)
        self.option.add_named(box2, "custom")

        # default buttons
        buttons = [
            ("8x8", self.__handler.game_option_8x8),
            ("16x16", self.__handler.game_option_16x16),
            ("24x16", self.__handler.game_option_24x16),
            ("Custom", self._to_custom)
        ]
        for label, cb in buttons:
            btn = Gtk.Button(label=label)
            btn.connect("clicked", cb)
            btn.set_size_request(270, 200)
            grid.insert(btn, -1)

    def _init_game_stack(self):
        self.gamebox = GameBox()
        self.stack.add_named(self.option, "options")
        self.stack.add_named(self.gamebox, "gamebox")
        GameHandler.Menu = self.on_menu
        self.option.connect("hide", self._option_hidden)

    def _from_custom(self, *args):
        self.option.set_visible_child_name("main")

    def _to_custom(self, *args):
        self.option.set_visible_child_name("custom")

    def on_menu(self, *args):
        self.option.show()
        self.stack.set_visible_child_name("options")
        self.update_subtitle("")

    def _option_hidden(self, *args):
        sub = "Tiles: {0}x{1}, Mines: {2}%".format(*GameHandler.game_dimension)
        self.update_subtitle(sub)
        self.stack.set_visible_child_name("gamebox")
        self.gamebox._setup_page()
        self.gamebox.start()
