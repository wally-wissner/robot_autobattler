import json

from config import absolute_path


filename_settings = absolute_path("player_data/settings.json")


class SettingsManager:
    def __init__(self):
        self.dict = None

    def _get_setting(self, setting: str) -> int | list[int, int]:
        return self.dict[setting]["current"]

    def _set_setting(self, setting: str, value) -> None:
        self.dict[setting]["current"] = value
        self.save()

    def load(self):
        with open(filename_settings, "r", encoding="utf-8") as f:
            self.dict = json.load(f)

    def save(self):
        with open(filename_settings, "w", encoding="utf-8") as f:
            json.dump(self.dict, f)

    def restore_defaults(self):
        for setting in self.dict:
            self.dict[setting]["current"] = self.dict[setting]["default"]
        self.save()

    @property
    def resolution(self) -> tuple[int, int]:
        return tuple(self._get_setting("resolution"))

    @resolution.setter
    def resolution(self, value: tuple) -> None:
        self._set_setting("resolution", value)

    @property
    def width(self):
        return self.resolution[0]

    @property
    def height(self):
        return self.resolution[1]
