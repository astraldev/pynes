
import gi
import sys

gi.require_version("Gtk", '4.0')
gi.require_version("Adw", "1")

from pynes import VERSION
from pynes.GameApplication import Game

if __name__ == "__main__":
  app = Game()
  if len(sys.argv) > 1 and sys.argv[1] == "--version":
    print(f"GGate: v{VERSION}")
    sys.exit(0)

  app.run()
