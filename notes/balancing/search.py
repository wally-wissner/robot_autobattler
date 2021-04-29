import numpy as np
import pandas as pd
from sklearn.metrics import r2_score


def damage(AP, base_accuracy, power, cost, accuracy_penalty, armor, shields, evasion):
    return max(power - armor, 0) * max(np.floor(AP / cost) - shields, 0) * max(min(base_accuracy - accuracy_penalty - evasion, 1), 0)


def expected_damage(
    AP, base_accuracy,
    power_R, cost_R, accuracy_R,
    power_M, cost_M, accuracy_M,
    power_L, cost_L, accuracy_L,
    armor, shields, evasion,
    weak=.8, neutral=1, strong=1.2
):
    df = pd.DataFrame(columns=["Offense", "Defense", "Target", "Actual"])

    df.loc[len(df)] = ["Railgun", "Armor", weak, damage(AP, base_accuracy, power_R, cost_R, accuracy_R, armor, 0, 0)]
    df.loc[len(df)] = ["Railgun", "Shields", strong, damage(AP, base_accuracy, power_R, cost_R, accuracy_R, 0, shields, 0)]
    df.loc[len(df)] = ["Railgun", "Evasion", neutral, damage(AP, base_accuracy, power_R, cost_R, accuracy_R, 0, 0, evasion)]
    df.loc[len(df)] = ["Missile", "Armor", strong, damage(AP, base_accuracy, power_M, cost_M, accuracy_M, armor, 0, 0)]
    df.loc[len(df)] = ["Missile", "Shields", neutral, damage(AP, base_accuracy, power_M, cost_M, accuracy_M, 0, shields, 0)]
    df.loc[len(df)] = ["Missile", "Evasion", weak, damage(AP, base_accuracy, power_M, cost_M, accuracy_M, 0, 0, evasion)]
    df.loc[len(df)] = ["Laser", "Armor", neutral, damage(AP, base_accuracy, power_L, cost_L, accuracy_L, armor, 0, 0)]
    df.loc[len(df)] = ["Laser", "Shields", weak, damage(AP, base_accuracy, power_L, cost_L, accuracy_L, 0, shields, 0)]
    df.loc[len(df)] = ["Laser", "Evasion", strong, damage(AP, base_accuracy, power_L, cost_L, accuracy_L, 0, 0, evasion)]

    if df["Actual"].mean() > 0:
        df["Actual"] = df["Actual"] / df["Actual"].mean()

    return df


def random_search(iterations, swaps=1, seed=0):
    np.random.seed(seed)

    all_params = {
        "AP": range(8, 20),
        "base_accuracy": np.arange(.75, 1, .01),
        "power_R": range(1, 20),
        "cost_R": range(1, 20),
        "accuracy_R": np.arange(0, .25, .01),
        "power_M": range(1, 20),
        "cost_M": range(1, 20),
        "accuracy_M": np.arange(0, .25, .01),
        "power_L": range(1, 20),
        "cost_L": range(1, 20),
        "accuracy_L": [-80000],
        "armor": range(1, 5),
        "shields": [1],
        "evasion": np.arange(0, .25, .01)
    }

    # params_best = {key: np.random.choice(all_params[key]) for key in all_params}
    params_best = {'AP': 18, 'base_accuracy': 0.79, 'power_R': 5, 'cost_R': 3, 'accuracy_R': 0.05, 'power_M': 10, 'cost_M': 4, 'accuracy_M': 0.24, 'power_L': 7, 'cost_L': 6, 'accuracy_L': -80000, 'armor': 2, 'shields': 1, 'evasion': 0.22}

    ed = expected_damage(**params_best)
    r2_best = r2_score(ed["Target"], ed["Actual"])

    for _ in range(iterations):
        params = params_best.copy()
        for _ in range(swaps):
            new_param = np.random.choice(list(params.keys()))
            params[new_param] = np.random.choice(all_params[new_param])
        ed_1 = expected_damage(**params)

        params_0 = params.copy()
        params_0["armor"] = 0
        params_0["shields"] = 0
        params_0["evasion"] = 0
        params_0["strong"] = 1
        params_0["weak"] = 1
        ed_0 = expected_damage(**params_0)

        ed = pd.concat([ed_0, ed_1])

        r2 = r2_score(ed["Target"], ed["Actual"])

        if r2 > r2_best:
            r2_best = r2
            params_best = params
            print(ed)
            print(params)
            print(f"R^2: {r2}")


if __name__ == "__main__":
    random_search(100000000, swaps=3, seed=8)
