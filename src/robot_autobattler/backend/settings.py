import json

from config import absolute_path


filename_settings = absolute_path("player_data/settings.json")


class SettingsManager:
    def __init__(self, application):
        self.application = application
        self.dict = None

    # @property
    # def resolution(self):
    #     return self._resolution
    #
    # @resolution.setter
    # def resolution(self, value):
    #     pass

    @property
    def width(self):
        return self.resolution[0]

    @property
    def height(self):
        return self.resolution[1]

    def __getattr__(self, item):
        if item in self.__dict__:
            attr = self.__dict__[item]
        else:
            attr = self.dict[item]["current"]
        return attr

    def load(self):
        with open(filename_settings, "r", encoding="utf-8") as f:
            self.dict = json.load(f)

    def save(self):
        with open(filename_settings, "w", encoding="utf-8") as f:
            json.dump(self.dict, f)

    def restore_defaults(self):
        for setting in self.settings:
            self.settings[setting]["current"] = self.settings[setting]["default"]
        self.save()
