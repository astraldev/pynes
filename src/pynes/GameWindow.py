#!/usr/bin/env python3
from threading import Thread
import gi, os
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib, Gio
from random import choice, randint
from time import sleep
from timeutilities import Time
from pynes.utils import check_config, setup_css_file
from pynes.constants import ANIMATE, CSS_FILES, MENU_XML, AnimationDir, LB_TEXT, LEADERBOARD_FILE, ICON
import csv

class GameOptionBox(Gtk.Box):
    def __init__(self, tilebox, *args):
        super().__init__(*args, spacing=10)
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
        GameHandler.MainWindow.connect("notify::is-active", self.lost_focus)

        self.pause_button.set_sensitive(True)
        self.pause = False
        self.paused_by = ""

    def lost_focus(self, *args):

        if GameHandler.GameOver:
            return
        self.paused_by = "window" if not self.paused else "btn"
        if self.paused_by == "btn" and self.pause:
            return
        if not args[0].is_active():
            self.paused(ps=True)
        else:
            self.paused(ps=False)

    def _btn_pause(self, *args):
        self.paused_by = "btn"
        self.paused(not self.pause)

    def paused(self, ps=False):
        if not self.pause or ps:
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
        
        opened = len(GameHandler.OpenedTiles) if len(
            GameHandler.OpenedTiles) > 9 else "0" + str(len(GameHandler.OpenedTiles))
        self.s_tiles_label.set_text("{0} | {1}".format(
            opened, len(GameHandler.WinningTiles)))
        self.s_flagged_label.set_text("{0} | {1}".format(
            len(GameHandler.FlaggedTiles), len(GameHandler.MineTiles)))
        return True

    def _right_clicked(self, gesture, *event):
        # Right click event
        if gesture.get_button() == Gdk.BUTTON_SECONDARY:
            gesture.get_widget()._toogle_icon()
            self.s_flagged_label.set_text("{} | {}".format(len(GameHandler.FlaggedTiles), len(GameHandler.MineTiles)))

    def start(self, *args):
        self.s_time_label.set_text("00:00")
        self.s_tiles_label.set_text(
            "0 | {}".format(len(GameHandler.WinningTiles)))
        self.s_flagged_label.set_text(
            "0 | {}".format(len(GameHandler.MineTiles)))

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

        if self.pause:
            return True

        if GameHandler.AnimationOver is False:
            return True

        self.s_time.tick()
        mins = self.s_time.minute
        secs = self.s_time.second
        if mins < 10:
            mins = "0" + str(mins)
        if secs < 10:
            secs = "0" + str(secs)
        hour = self.s_time.hour
        if hour < 1:
            hour = ""
        else:
            hour = f"{hour}:"

        mins, secs = str(mins), str(secs)
        tm = f"{hour}{mins}:{secs}"
        self.s_time_label.set_text(tm)
        GameHandler.CurrentTime = tm

        return True


class GameBox(Gtk.Box, GameHandler):
    def _setup_page(self, *args):
        children = []
        _first_child = self.get_first_child()

        if not _first_child is None:
            children.append(_first_child)
            while _first_child.get_next_sibling():
                _first_child = _first_child.get_next_sibling()
                children.append(_first_child)
        
        for child in children: self.remove(child)

        self.tile_box = TileBox()
        self.opt = GameOptionBox(self.tile_box)
        self.opt.restart_button.connect("clicked", self.on_restart)

        self.tile_box.set_margin_start(10)
        self.tile_box.set_margin_top(10)
        self.tile_box.set_margin_bottom(10)

        self.append(self.tile_box)
        self.append(self.opt)

    def __init__(self, *args):
        super().__init__(*args, spacing=5)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.dimension = self.get_game_dimension()

    def start(self, *args):
        GameHandler.Tiles = []
        GameHandler.WinningTiles = []
        GameHandler.OpenedTiles = []
        GameHandler.GameOver = False
        GameHandler.MineTiles = []
        GameHandler.FlaggedTiles = []
        GameHandler.AnimationOver = False
        GameHandler.CurrentTime = ""

        self.create_arrangement()
        self.opt.start()
        self.opt.menu_button.connect("clicked", GameHandler.Menu)
        self.show()
        Thread(target=self._animate).start()

    def _animate(self, *args):
        if not ANIMATE: 
            GameHandler.AnimationOver = True
            return
        length_of_tiles = len(GameHandler.Tiles)

        def _(tile, nm):
            sleep(0.025)
            tile.set_name(nm)

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


class LeaderBoard(Gtk.Window):
    def _get_content(self, *args):
        return self.reader[1:]

    def _get_titles(self, *args):
        return self.reader[0]

    def fill_store(self):
        for ind, items in enumerate(self._get_content(), 0):
            if self.location == ind:
                self.location = self.store.append()
                self.store.insert_with_values(ind, (0,1,2,3,4), items)
                continue
            self.store.insert_with_values(ind, (0,1,2,3,4), items)


    def fill_columns(self, *args):
        for index, text in enumerate(self._get_titles()):
            renderer_text = Gtk.CellRendererText()
            column_text = Gtk.TreeViewColumn(text, renderer_text, text=index)
            self.treeview.append_column(column_text)

        model = self.treeview.get_model()
        self.treeview.show()

        if self.location is not None and type(self.location) is not int:
            loc = model.get_path(self.location)
            if loc is not None:
                self.treeview.set_cursor(loc)

    def __init__(self, loc, *args):
        super().__init__(*args)
        self.set_title("Leaderboard")

        self.reader = list(csv.reader(open(LEADERBOARD_FILE)))

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scroll = Gtk.ScrolledWindow()

        self.reset_button = Gtk.Button(label="Reset")
        self.reset_button.add_css_class('destructive-action')

        header_bar = Gtk.HeaderBar()
        header_bar.pack_start(self.reset_button)

        self.location = loc
        self.store = Gtk.ListStore(str, str, str, str, str)
        self.fill_store()
        self.treeview = Gtk.TreeView(model=self.store)
        scroll.set_child(self.treeview)

        box.append(scroll)
        scroll.set_vexpand(True)
        scroll.set_hexpand(True)

        self.set_titlebar(header_bar)
        self.set_child(box)

        self.set_modal(True)
        self.set_default_size(300, 350)
        self.set_transient_for(GameHandler.MainWindow)
        self.set_resizable(False)
        self.connect('hide', self._hide)
        self.reset_button.connect('clicked', self.on_reset )
        self.fill_columns()
        self.present()
    
    def on_reset(self, *args):
        open(LEADERBOARD_FILE, 'w').write(LB_TEXT)
        self._hide()

    def _hide(self, *args):
        self.destroy()
        open(LEADERBOARD_FILE, "w").write(LB_TEXT)


class OptionMenu(Gtk.Stack, GameHandler):
    def __init__(self, *args):
        super().__init__(*args)

        self.grid = Gtk.FlowBox()
        self.grid.set_max_children_per_line(2)
        self.grid.set_min_children_per_line(2)
        self.grid.set_selection_mode(Gtk.SelectionMode.NONE)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box_inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box2_inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.grid2 = Gtk.Grid()
        self.grid2.set_column_homogeneous(True)
        self.grid2.set_row_homogeneous(True)

        button1 = Gtk.Button(label="8x8")
        button2 = Gtk.Button(label="16x16")
        button3 = Gtk.Button(label="24x16")
        button6 = Gtk.Button(label="Custom")

        row_label = Gtk.Label(label="Rows")
        row_spin = Gtk.SpinButton()
        adjustment = Gtk.Adjustment(
            upper=32, value=24, lower=3, step_increment=1, page_increment=5)
        row_spin.set_adjustment(adjustment)

        #  Set Size of all items by setting 1
        row_label.set_size_request(90, 30)

        self.grid2.attach(row_label, 0, 0, 1, 1)
        self.grid2.attach(row_spin, 1, 0, 1, 1)

        col_label = Gtk.Label(label="Columns")
        col_spin = Gtk.SpinButton()
        adjustment = Gtk.Adjustment(
            upper=22, value=16, lower=3, step_increment=1, page_increment=5)
        col_spin.set_adjustment(adjustment)

        self.grid2.attach(col_label, 0, 1, 1, 1)
        self.grid2.attach(col_spin, 1, 1, 1, 1)

        mine_label = Gtk.Label(label="Mine ( % )")
        mine_spin = Gtk.SpinButton()
        adjustment = Gtk.Adjustment(
            upper=90, value=15, lower=1, step_increment=1, page_increment=5)
        mine_spin.set_adjustment(adjustment)
        self.grid2.attach(mine_label, 0, 2, 1, 1)
        self.grid2.attach(mine_spin, 1, 2, 1, 1)

        back_btn = Gtk.Button(label="Back")
        back_btn.connect("clicked", self._from_custom)

        play_btn = Gtk.Button(label="Go")
        play_btn.connect("clicked", self.game_option_custom,
                         row_spin, col_spin, mine_spin)

        self.grid2.attach(play_btn, 1, 3, 1, 1)
        self.grid2.attach(back_btn, 0, 3, 1, 1)
        self.grid2.set_column_spacing(2)
        self.grid2.set_row_spacing(2)

        self.grid.insert(button1, 0)
        self.grid.insert(button2, -1)
        self.grid.insert(button3, -1)
        self.grid.insert(button6, -1)

        button1.connect("clicked", self.game_option_8x8)
        button1.set_size_request(270,200)
        button2.connect("clicked", self.game_option_16x16)
        button2.set_size_request(270,200)
        button3.connect("clicked", self.game_option_24x16)
        button2.set_size_request(270,200)
        button6.connect("clicked", self._to_custom)
        button6.set_size_request(270,200) 

        self.box_inner.append(self.grid)
        self.grid.set_vexpand(True)
        self.grid.set_hexpand(True)
        self.grid.set_valign(Gtk.Align.CENTER)
        self.grid.set_halign(Gtk.Align.CENTER)
        # self.grid.set_margin_top(40)
        # self.grid.set_margin_end(40)
        # self.grid.set_margin_start(40)
        # self.grid.set_margin_bottom(40)

        self.box.append(self.box_inner)
        self.box_inner.set_vexpand(True)
        self.box_inner.set_hexpand(True)
        # self.box_inner.set_margin_top(40)
        # self.box_inner.set_margin_end(40)
        # self.box_inner.set_margin_start(40)
        # self.box_inner.set_margin_bottom(40)

        self.add_named(self.box, "main")

        self.box2_inner.append(self.grid2)

        self.grid2.set_vexpand(True)
        self.grid2.set_hexpand(True)
        # self.grid2.set_margin_top(30)
        # self.grid2.set_margin_end(30)
        # self.grid2.set_margin_start(30)
        # self.grid2.set_margin_bottom(30)
        self.grid2.set_valign(Gtk.Align.CENTER)
        self.grid2.set_halign(Gtk.Align.CENTER)

        self.box2.append(self.box2_inner)
        
        self.box2_inner.set_vexpand(True)
        self.box2_inner.set_hexpand(True)
        self.box2_inner.set_margin_top(30)
        self.box2_inner.set_margin_end(30)
        self.box2_inner.set_margin_start(30)
        self.box2_inner.set_margin_bottom(30)

        self.add_named(self.box2, "custom")

    def _from_custom(self, *args):
        self.set_visible_child(self.box)

    def _to_custom(self, *args):
        self.set_visible_child(self.box2)


class GameStack(Gtk.Stack):
    def __init__(self, *args, **kwargs):
        # Order
        # - option
        # - game page

        super().__init__(*args, **kwargs)
        self.option = OptionMenu()
        self.gamebox = GameBox()
        self.add_named(self.option, "options")
        self.add_named(self.gamebox, "gamebox")
        GameHandler.Menu = self.on_menu
        # self.option.connect("size-allocate", self.option_resized)
        # self.option.connect('realize', self.option_resized)

        self.option.connect("hide", self._option_hidden)
        # self.connect("size-allocate", self.resized)

    def on_menu(self, *args):
        self.option.show()
        self.set_visible_child_name("options")
        GameHandler.MainWindow.header_bar.set_subtitle("")

    def _option_hidden(self, *args):
        sub = "Tiles: {0}x{1}, Mines: {2}%".format(*GameHandler.game_dimension)
        GameHandler.MainWindow.header_bar.set_subtitle(sub)
        self.set_visible_child_name("gamebox")
        self.gamebox._setup_page()
        self.gamebox.start()

    def option_resized(self, *args):
        GLib.timeout_add_seconds(1, self._option_resize_thread)

    def _option_resize_thread(self):
        # 90% when at width is 720 or less
        # 70% when at width is 720 or more
        sizes = [GameHandler.MainWindow.get_width(), GameHandler.MainWindow.get_height()]
        prev = sizes
        if sizes[0] <= 720:
            sizes[0] = sizes[0]*0.9
        elif sizes[0] > 720:
            sizes[0] = sizes[0]*0.75

        if sizes[1] <= 720:
            sizes[1] = sizes[1]*0.9
        elif sizes[1] > 720:
            sizes[1] = sizes[1]*0.75

        sizes = [int(sizes[0]), int(sizes[1])]
        margin = [int((GameHandler.MainWindow.get_width()-sizes[0])/2)-10,
                  int((GameHandler.MainWindow.get_height() - sizes[1])/2)-10]
        self.option.set_margin_top(margin[1])
        self.option.set_margin_bottom(margin[1])
        self.option.set_margin_end(margin[0])
        self.option.set_margin_start(margin[0])

        return True

    def resized(self, *args):
        size = self.get_allocated_size()[0]
        size = [size.width, size.height]
        if size[0] < 470 or size[1] < 370:
            self.set_size_request(570, 470)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_child(GameStack())
        GameHandler.MainWindow = self
        self.header_bar = Gtk.HeaderBar()

        # title_widget = Gtk.Box()
        # title_label = Gtk.Label(label="Pynes")
        # self.subtitle_label = Gtk.Label()
        # self.subtitle_label.set_name('subtitle')

        # title_widget.set_orientation(Gtk.Orientation.VERTICAL)
        # title_widget.append(title_label)
        # title_widget.append(self.subtitle_label)

        self.set_title("pynes")
        self.header_bar.set_show_title_buttons(True)

        self.header_bar.set_subtitle = lambda x : self.set_title(f"pynes - {x}" if x else " pynes " )
        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        menu = builder.get_object("app-menu")
        button = Gtk.MenuButton.new()
        # button.set_name('menu-button')
        button.set_direction(Gtk.ArrowType.NONE)
        popover = Gtk.PopoverMenu.new_from_model(menu)
        button.set_popover(popover)
        self.set_titlebar(self.header_bar)
        self.header_bar.pack_start(button)
        self.set_default_size(570, 470)
        self.poped_up = False


class Game(Gtk.Application, GameHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.astralco.pyne", **kwargs)
        self.window = None

    def do_startup(self, *args):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.about)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)

        action.connect("activate", self.on_quit)
        self.add_action(action)
        self.set_accels_for_action('app.quit', ["<Ctrl>Q"])

        action = Gio.SimpleAction.new("leaderboard", None)
        action.connect("activate", self.on_leaderboard)
        self.add_action(action)
        self.set_accels_for_action('app.leaderboard', ['<Ctrl>L'])

        action = Gio.SimpleAction.new("preferences", None)
        action.connect("activate", self.on_pref)
        self.add_action(action)
        self.set_accels_for_action('app.preferences', ['<Ctrl>P'])
    
    def on_pref(self, *args):
        pref = PrefHandler(self.window)
        pref.start()

    def on_leaderboard(self, *args):
        self._organize_config()
        LeaderBoard(1).show()

    def about(self, *args):
        dialog = Gtk.AboutDialog(title="Pyne", transient_for=self.window)
        dialog.set_version("3.0.0")
        dialog.set_name("About")
        dialog.set_program_name("Pyne")
        dialog.set_authors(["Ekure Nyong"])
        dialog.set_comments("PyGtk mine game")
        dialog.set_license_type(Gtk.License.LGPL_3_0)
        dialog.present()

    def do_activate(self, *args):
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = MainWindow(application=self)
            self.window.connect("destroy", self.on_quit)
            self.window.set_icon_name("pynes")
            self.add_window(self.window)
        self.window.present()
        # self.window.show()

    def on_quit(self, *args):
        os.system(f"rm {CSS}")
        self.quit()


if __name__ == "__main__":
    check_config()
    css = Gtk.CssProvider()
    CSS, COLOR = setup_css_file()
    css.load_from_path(CSS)
    screen = Gdk.Display.get_default()
    Gtk.StyleContext().add_provider_for_display(screen, css, 600)
    app = Game()
    app.run()