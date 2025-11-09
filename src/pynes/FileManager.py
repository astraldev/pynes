import os
import re
import json
from gi.repository import GLib

class FileManager:
    PREF_DIR = os.path.join(GLib.get_user_config_dir(), "pynes")
    PREF_FILE = os.path.join(PREF_DIR, "preferences.json")
    USER_THEME_FILE = os.path.join(PREF_DIR, "user_theme.css")
    DEFAULT_THEME_FILE = os.path.join(PREF_DIR, "default_theme.css")

    @staticmethod
    def ensure_dir() -> None:
        os.makedirs(FileManager.PREF_DIR, exist_ok=True)

    @staticmethod
    def read_json() -> dict:
        FileManager.ensure_dir()
        if not os.path.exists(FileManager.PREF_FILE):
            return {}
        try:
            with open(FileManager.PREF_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {}

    @staticmethod
    def write_json(data: dict) -> None:
        FileManager.ensure_dir()
        with open(FileManager.PREF_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def read_text(path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    @staticmethod
    def write_text(path: str, content: str) -> None:
        FileManager.ensure_dir()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def reset_file(file_path: str) -> None:
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def write_theme(theme_data: dict) -> None:
        FileManager.ensure_dir()
        css_lines = [":root {"]
        for var, color in theme_data.items():
            css_lines.append(f"    {var}: {color};")
        css_lines.append("}")
        FileManager.write_text(FileManager.USER_THEME_FILE, "\n".join(css_lines))

    @staticmethod
    def read_theme() -> dict:
        """Merge default and user themes. User overrides default."""
        pattern = r"(--[\w-]+)\s*:\s*([^;]+);"

        def parse_css(path: str) -> dict:
            css = FileManager.read_text(path)
            return {name.strip(): value.strip() for name, value in re.findall(pattern, css)}

        default_theme = parse_css(FileManager.DEFAULT_THEME_FILE)
        user_theme = parse_css(FileManager.USER_THEME_FILE)
        return {**default_theme, **user_theme}
    
    def load_data_file():
        pass
