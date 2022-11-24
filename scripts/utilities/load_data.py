import json

from scripts.utilities import enums


path_badges = "../../assets/item_data/badges.json"


def load_badges():
    with open(path_badges) as f:
        d = json.load(f)
        for item in d:
            item["rarity"] = enums.ERarity[item["rarity"]]
            item["stat_modifiers"] = [
                [enums.EStat[stat], enums.EOperation[operation], value]
                for stat, operation, value in item["stat_modifiers"]
            ]
    return d


d = load_badges()
print(d)
