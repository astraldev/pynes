import re
from gi.repository import Gtk, Adw, Gdk
from pynes.Blocks.Tile import Tile
from pynes.Preferences import Preferences

__ColorMap = {
    "--text-color": "Text color",
    "--tile-bg": "Unmodified Tile Color",
    "--tile-flagged": "Flagged Tile Color",
    "--tile-opened": "Opened Tile Color",
    "--mine-opened": "Mine Tile Color",
    "--unsure-flagged": "Unsure Tile Color",
}

class PreferenceDialog(Adw.PreferencesDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Preferences.hydrate()

        # Enable / Disable animations
        should_animate_switch = Adw.SwitchRow()
        should_animate_switch.set_title("Enable animations")
        should_animate_switch.set_active(Preferences.AnimationsEnabled)
        should_animate_switch.connect("activate", self._animation_pref_changed)

        # General settings
        general_pref_group = Adw.PreferencesGroup(title="General")
        general_pref_group.add(should_animate_switch)

        # Tile colors
        self.colors = self._set_up_colors()
        self.color_rows = []

        for color in self.colors:
            if color not in __ColorMap: continue  # noqa: E701

            rgb_color = Gdk.RGBA()
            rgb_color.parse(self.colors[color])

            color_picker = Gtk.ColorDialogButton()
            color_picker.set_rgba(rgb_color)
            color_picker.connect("notify::rgba", self.color_changed, color)

            color_row = Adw.ActionRow()
            color_row.add_suffix(color_picker)
            color_row.set_title(__ColorMap[color])

            self.color_rows.append(color_row)
        
        color_pref_group = Adw.PreferencesGroup(title="Interface colors")
        [color_pref_group.add(color_row) for color_row in self.color_rows]

        # Preference page
        main_pref_page = Adw.PreferencesPage()
        main_pref_page.add(general_pref_group)
        main_pref_page.add(color_pref_group)

        self.add(main_pref_page)
        
        # Grid Preview
        tile_preview_grid = Gtk.Grid()

        tile_1 = Tile.dummy()
        tile_2 = Tile.dummy(state=False)
        tile_3 = Tile.dummy(mine=True)
        tile_4 = Tile.dummy(flag=True)
        tile_5 = Tile.dummy(question=True)
        tile_6 = Tile.dummy(is_active=True)
        
        tile_preview_grid.attach(tile_1, 0, 0, 1, 1)
        tile_preview_grid.attach(tile_2, 1, 0, 1, 1)
        tile_preview_grid.attach(tile_3, 2, 0, 1, 1)
        tile_preview_grid.attach(tile_4, 1, 1, 1, 1)
        tile_preview_grid.attach(tile_5, 0, 1, 1, 1)
        tile_preview_grid.attach(tile_6, 2, 1, 1, 1)

        tile_preview_grid.set_vexpand(False)
        tile_preview_grid.set_hexpand(True)

        tile_preview_grid.set_size_request(300, 200)

        # reset_btn.connect('clicked', self.reset_all)
    
    def _animation_pref_changed(self, button: Adw.SwitchRow, *args):
        Preferences.AnimationsEnabled = button.get_active()
        Preferences.persist()

    def _set_up_colors(self):
        css_var_pattern = r"(--[\w-]+)\s*:\s*([^;]+);"

        # Read default color set
        default_colors = ""

        # Read user color set
        data = ""

        default_color_map = { name.strip(): value.strip() for name, value in re.findall(css_var_pattern, default_colors) }
        user_color_map = { name.strip(): value.strip() for name, value in re.findall(css_var_pattern, data) }

        return { **default_color_map, **user_color_map }

    # https://gist.github.com/astraldev/f8534e25f195ee959d5c5709750c327a
    def __rgb_to_hex(self, color, *args):
        hex_value = '#%02x%02x%02x' % (int(color.red*255), int(color.green*255), int(color.blue*255))
        return hex_value

    def color_changed(self, c_button: Gtk.ColorDialogButton, key, *args):
        rgba = c_button.get_rgba()
        Preferences.UserColorThemeData[key] = self.__rgb_to_hex(rgba)
        Preferences.persist()
    
    def refresh_preferences():
        # Set the animation setting
        # Reset the colors
        pass

    def reset_all(self, *res):
        Preferences.reset()
        self.refresh_preferences()
