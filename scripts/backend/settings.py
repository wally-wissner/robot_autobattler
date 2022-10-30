import json


filename_settings = "../../data/settings.json"


class Settings:
    def __init__(self):
        self.dict = None

        # self.resolution = None
        # self.fps = None
        # self.volume_overall = None
        # self.volume_music = None
        # self.volume_sfx = None

    # @property
    # def resolution(self):
    #     return self._resolution
    #
    # @resolution.setter
    # def resolution(self, value):
    #     pass

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            return self.dict[item]["current"]

    def load(self):
        with open(filename_settings, 'r') as f:
            self.dict = json.load(f)

    def save(self):
        with open(filename_settings, 'w') as f:
            json.dump(self.dict, f)

    def restore_defaults(self):
        for setting in self.settings:
            self.settings[setting]["current"] = self.settings[setting]["default"]
        self.save()
