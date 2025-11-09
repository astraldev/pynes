import os
from pynes.FileManager import FileManager

DefaultPreferences = {
    "animations_enabled": False,
    "user_modified_colors": False,
    "user_color_theme": {}
}

class Preferences:
    AnimationsEnabled = False
    DefaultColorThemeData = {}
    UserModifiedColors = False
    UserColorThemeData = {}

    @staticmethod
    def init():
        FileManager.ensure_config_dir()
        
        # Initialize preference file if it doesn't exist
        if not os.path.exists(FileManager.PREF_FILE):
            FileManager.write_user_config(DefaultPreferences)

        try:
            prefs = FileManager.read_user_config()

            if not isinstance(prefs, dict):
                raise ValueError("Invalid preference file format")
            
            merged_prefs = DefaultPreferences.update(prefs)
            FileManager.write_user_config(merged_prefs)
        except (ValueError, KeyError):
            # Reset if file is corrupted
            Preferences.reset()

        Preferences.DefaultColorThemeData = FileManager.read_theme_data()

    @staticmethod
    def hydrate():
        """Load preferences from the config file."""
        Preferences.init()  # Ensure files exist first

        merged_pref_data = { **DefaultPreferences }
        
        try:
            prefs = FileManager.read_user_config()
            merged_pref_data.update(prefs)

        # Reset the file if reading user config failed
        except Exception:
            Preferences.reset()

        Preferences.AnimationsEnabled = merged_pref_data.get("animations_enabled", False)
        Preferences.UserModifiedColors = merged_pref_data.get("user_modified_colors", False)
        Preferences.UserColorThemeData = merged_pref_data.get("user_color_theme", {})
        Preferences.DefaultColorThemeData = FileManager.read_theme_data()

    @staticmethod
    def persist():
        """Save current preferences to the config file."""
        FileManager.ensure_config_dir()
        
        prefs = { **DefaultPreferences }
        prefs["animations_enabled"] = Preferences.AnimationsEnabled
        prefs["user_modified_colors"] = Preferences.UserModifiedColors
        prefs["user_color_theme"] = Preferences.UserColorThemeData
        
        FileManager.write_user_config(prefs)
        FileManager.write_theme(Preferences.UserColorThemeData)

    @staticmethod
    def reset():
        """Reset all preferences to default values."""
        # Reset in-memory values
        Preferences.AnimationsEnabled = DefaultPreferences["animations_enabled"]
        Preferences.UserModifiedColors = DefaultPreferences["user_modified_colors"]
        Preferences.UserColorThemeData = DefaultPreferences["user_color_theme"]
        FileManager.write_user_config(DefaultPreferences)
        
        # Remove the user theme file
        if os.path.exists(FileManager.USER_THEME_FILE):
            FileManager.reset_file(FileManager.USER_THEME_FILE)
        
        # Reload the default theme data
        Preferences.DefaultColorThemeData = FileManager.read_theme_data()