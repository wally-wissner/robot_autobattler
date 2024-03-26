# pylint: disable=broad-exception-caught

import unittest

from frontend.application import application
from frontend.scenes import scene_map


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.application = application
        self.application.load_scene_map(scene_map)

    def test_quit(self):
        try:
            pass
            # application.run()
            # application.quit()
        except Exception as e:
            self.fail(f"Application encountered an error: {e}")
