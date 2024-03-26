"""
Run this script to begin playing the game.
"""

from frontend.application import application
from frontend.scenes import scene_map

if __name__ == "__main__":
    application.load_scene_map(scene_map)
    application.run()
