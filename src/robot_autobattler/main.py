"""
Run this script to begin playing the game.
"""

# Ignore warning for Singleton decorator.
# pylint: disable=no-member

from frontend.scenes import Application


if __name__ == "__main__":
    application = Application.instance()
    application.run()
