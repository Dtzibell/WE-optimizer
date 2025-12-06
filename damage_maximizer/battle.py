import numpy as np
import urllib.request as rq
import json
import re
from copy import deepcopy
import pprint
from functools import wraps


class DamageCalculator:
    def with_available_sp(self, sp):
        self.available_sp = sp
        return self

    def with_helmetlvl(self, lvl):
        self.helmetlvl = lvl
        return self

    def with_chestlvl(self, lvl):
        self.chestlvl = lvl
        return self

    def with_gloveslvl(self, lvl):
        self.gloveslvl = lvl
        return self

    def with_pantslvl(self, lvl):
        self.pantslvl = lvl
        return self

    def with_bootslvl(self, lvl):
        self.bootslvl = lvl
        return self

    def with_weaponlvl(self, lvl):
        self.weaponlvl = lvl
        return self

    def with_ammolvl(self, lvl):
        self.ammolvl = lvl
        return self

    def with_mu_hqlvl(self, lvl):
        self.mu_hqlvl = lvl
        return self

    def with_country_bunkerlvl(self, lvl):
        self.country_bunkerlvl = lvl
        return self

    def with_military_baselvl(self, lvl):
        self.military_baselvl = lvl
        return self

    def with_country_orderlvl(self, lvl):
        self.country_orderlvl = lvl
        return self

    def with_mu_orderlvl(self, lvl):
        self.mu_orderlvl = lvl
        return self

    def with_resistance(self, res):
        self.resistance = res
        return self

    def with_pill(self, pill):
        self.is_pill_multiplier = 0.8
        self.is_pill = pill
        return self

    def with_core_region(self, core_region):
        self.is_core_region_multiplier = 0.15
        self.is_core_region = core_region
        return self

    def with_ally(self, ally):
        self.is_ally_multiplier = 0.1
        self.is_ally = ally
        return self

    def with_sworn_enemy(self, sworn_enemy):
        self.is_sworn_enemy_multiplier = 0.1
        self.is_sworn_enemy = sworn_enemy
        return self

    def with_region_not_linked(self, region_not_linked):
        self.is_region_not_linked_multiplier = -0.25
        self.is_region_not_linked = region_not_linked
        return self

    def with_attacking_region_lost(self, attacking_region_lost):
        self.is_attacking_region_lost_multiplier = -0.25
        self.is_attacking_region_lost = attacking_region_lost
        return self

    def with_per_hour(self, per_hour):
        self.per_hour = per_hour
        return self

    def __init__(self):
        # self.pull_gear_from_api("items.json")
        self.gear = DamageCalculator.get_gear("items.json")
        self.equipment = self.get_equipment()
        (
            self.helmet,
            self.chest,
            self.gloves,
            self.pants,
            self.boots,
            self.ammo,
            self.weapons,
        ) = self.separate_eq()
        self.country_bunker = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.25}
        self.military_base = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.25}
        self.country_order = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15}
        self.mu_order = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15}
        self.mu_hq = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2}
        self.weapon_hierarchy = ["knife", "gun", "rifle", "sniper", "tank", "jet"]
        self.ammo_hierarchy = ["lightAmmo", "ammo", "heavyAmmo"]
        self.base_stats: dict[str, float] = {
            "attack": 100,
            "precision": 50,
            "criticalChance": 10,
            "criticalDamages": 100,
            "armor": 0,
            "dodge": 0,
            "health": 50,
        }

        self.skill_growth = {
            "attack": 20,
            "precision": 0.05,
            "criticalChance": 0.05,
            "criticalDamages": 0.2,
            "armor": 0.04,
            "dodge": 0.04,
            "health": 10,
        }

        self.cost_of_upgrade = {
            "attack": 1,
            "precision": 1,
            "criticalChance": 1,
            "criticalDamages": 1,
            "armor": 1,
            "dodge": 1,
            "health": 1,
        }

        self.boni = {
            "attack": 0,
            "precision": 0,
            "criticalChance": 0,
            "criticalDamages": 0,
            "armor": 0,
            "dodge": 0,
            "health": 0,
        }

    @staticmethod
    def get_gear(path: str):
        with open(path, "r") as f:
            gear = json.load(f)
        return gear

    def get_equipment(self):
        c_gear = self.gear.copy()
        for k in self.gear.keys():
            if "dynamicStats" not in c_gear[k].keys() and not re.search(
                re.compile("ammo", re.IGNORECASE), k
            ):
                c_gear.pop(k)
        return self.gear

    def separate_eq(self):
        pants = {}
        chest = {}
        gloves = {}
        boots = {}
        helmet = {}
        ammo = {}
        weapons = {}
        for k in self.equipment.keys():
            if re.match(re.compile("pants.*"), k):
                pants.update({k: self.equipment[k]})
            if re.match(re.compile("chest.*"), k):
                chest.update({k: self.equipment[k]})
            if re.match(re.compile("gloves.*"), k):
                gloves.update({k: self.equipment[k]})
            if re.match(re.compile("boots.*"), k):
                boots.update({k: self.equipment[k]})
            if re.match(re.compile("helmet.*"), k):
                helmet.update({k: self.equipment[k]})
            if self.equipment[k]["type"] == "weapon":
                weapons.update({k: self.equipment[k]})
            if re.search(re.compile("ammo", re.IGNORECASE), k):
                _dict = {k: self.equipment[k]}
                ammo.update(_dict)
        return helmet, chest, gloves, pants, boots, ammo, weapons

    def post_init(self):
        self.helmet_stats = self.helmet[f"helmet{self.helmetlvl}"]["dynamicStats"]
        self.chest_stats = self.chest[f"chest{self.chestlvl}"]["dynamicStats"]
        self.gloves_stats = self.gloves[f"gloves{self.gloveslvl}"]["dynamicStats"]
        self.pants_stats = self.pants[f"pants{self.pantslvl}"]["dynamicStats"]
        self.boots_stats = self.boots[f"boots{self.bootslvl}"]["dynamicStats"]
        self.weapon_stats = self.weapons[self.weapon_hierarchy[self.weaponlvl - 1]][
            "dynamicStats"
        ]
        self.item_stats = [
            self.helmet_stats,
            self.chest_stats,
            self.gloves_stats,
            self.pants_stats,
            self.boots_stats,
            self.weapon_stats,
        ]
        self.bullets_stats = self.ammo[self.ammo_hierarchy[self.ammolvl - 1]][
            "flatStats"
        ]
        self.mu_hq_stats = self.mu_hq[self.mu_hqlvl]
        self.country_bunker_stats = self.country_bunker[self.country_bunkerlvl]
        self.military_base_stats = self.military_base[self.military_baselvl]
        self.country_order_stats = self.country_order[self.country_orderlvl]
        self.mu_order_stats = self.mu_order[self.mu_orderlvl]
        self.stats = self.base_stats
        self.convert_stats_to_proportion()
        self.update_boni()
        self.update_stats()

    def convert_stats_to_percent(self):
        self.stats["precision"] *= 100
        self.stats["armor"] *= 100
        self.stats["dodge"] *= 100
        self.stats["criticalChance"] *= 100
        self.stats["criticalDamages"] *= 100

    def convert_stats_to_proportion(self):
        self.stats["precision"] /= 100
        self.stats["armor"] /= 100
        self.stats["dodge"] /= 100
        self.stats["criticalChance"] /= 100
        self.stats["criticalDamages"] /= 100

    @staticmethod
    def setter(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.update_boni()
            self.update_stats()
            print(self.stats)

        return wrapper

    @setter
    def set_helmet_lvl(self, lvl):
        self.helmet_stats = self.helmet[f"helmet{lvl}"]["dynamicStats"]
        self.item_stats[0] = self.helmet_stats

    @setter
    def set_chest_lvl(self, lvl):
        self.chest_stats = self.chest[f"chest{lvl}"]["dynamicStats"]
        self.item_stats[1] = self.chest_stats

    @setter
    def set_gloves_lvl(self, lvl):
        self.gloves_stats = self.gloves[f"gloves{lvl}"]["dynamicStats"]
        self.item_stats[2] = self.gloves_stats

    @setter
    def set_pants_lvl(self, lvl):
        self.pants_stats = self.pants[f"pants{lvl}"]["dynamicStats"]
        self.item_stats[3] = self.pants_stats

    @setter
    def set_boots_lvl(self, lvl):
        self.boots_stats = self.boots[f"boots{lvl}"]["dynamicStats"]
        self.item_stats[4] = self.boots_stats

    @setter
    def set_ammo_lvl(self, lvl):
        self.ammolvl = lvl
        self.bullets_stats = self.ammo[self.ammo_hierarchy[self.ammolvl - 1]][
            "flatStats"
        ]

    @setter
    def set_weapon_lvl(self, lvl):
        self.weaponlvl = lvl
        self.weapon_stats = self.weapons[self.weapon_hierarchy[self.weaponlvl - 1]][
            "dynamicStats"
        ]
        self.item_stats[5] = self.weapon_stats

    @setter
    def set_mu_hq_lvl(self, lvl):
        self.mu_hqlvl = lvl
        self.mu_hq_stats = self.mu_hq[lvl]

    @setter
    def set_country_bunker_lvl(self, lvl):
        self.country_bunkerlvl = lvl
        self.country_bunker_stats = self.country_bunker[lvl]

    @setter
    def set_military_base_lvl(self, lvl):
        self.military_baselvl = lvl
        self.military_base_stats = self.military_base[lvl]

    @setter
    def set_country_order_lvl(self, lvl):
        self.country_orderlvl = lvl
        self.country_order_stats = self.country_order[lvl]

    @setter
    def set_mu_order_lvl(self, lvl):
        self.mu_orderlvl = lvl
        self.mu_order_stats = self.mu_order[lvl]

    @setter
    def set_resistance(self, res):
        self.resistance = res

    @setter
    def set_skill_points(self, n):
        self.available_sp = n

    @setter
    def set_per_hour(self, b):
        self.per_hour = b

    @setter
    def set_pill(self, b):
        self.is_pill = b

    @setter
    def set_core_region(self, b):
        self.is_core_region = b

    @setter
    def set_ally(self, b):
        self.is_ally = b

    @setter
    def set_sworn_enemy(self, b):
        self.is_sworn_enemy = b

    @setter
    def set_region_not_linked(self, b):
        self.is_region_not_linked = b

    @setter
    def set_attacking_region_lost(self, b):
        self.is_attacking_region_lost = b

    def update_stats(self):
        self.convert_stats_to_percent()
        self.stats: dict[str, float] = {
            k: self.base_stats[k] + self.boni[k] for k in self.base_stats.keys()
        }
        self.convert_stats_to_proportion()
        self.attack_bonus = (
            self.stats["attack"]
            * (
                1
                + self.is_pill * self.is_pill_multiplier
                + self.mu_hq_stats
                + self.bullets_stats["percentAttack"] / 100
                + self.mu_order_stats
                + self.country_order_stats
                + self.resistance / 100
                + self.country_bunker_stats
                + self.military_base_stats
                + self.is_core_region * self.is_core_region_multiplier
                + self.is_ally * self.is_ally_multiplier
                + self.is_sworn_enemy * self.is_sworn_enemy_multiplier
                + self.is_region_not_linked * self.is_region_not_linked_multiplier
                + self.is_attacking_region_lost
                * self.is_attacking_region_lost_multiplier
            )
            - self.stats["attack"]
        )
        print(self.attack_bonus)
        self.stats["attack"] += self.attack_bonus

    def update_boni(self):
        self.boni = {
            "attack": 0,
            "precision": 0,
            "criticalChance": 0,
            "criticalDamages": 0,
            "armor": 0,
            "dodge": 0,
            "health": 0,
        }
        for s in self.item_stats:
            for k in self.boni.keys():
                try:
                    self.boni[k] += (
                        s[k][0] + (s[k][1] - s[k][0]) / 4
                    )  # bottom quartile of the stats
                except KeyError:
                    pass

    def calculate_dmg(self, stats):
        precision_multiplier = (
            stats["precision"]  # chance to hit
            + (1 - stats["precision"])
            * 0.5  # chance to miss (which divides damage in half)
        )
        damage_times_precision = stats["attack"] * precision_multiplier
        dmg_per_attack = (1 - stats["criticalChance"]) * damage_times_precision + stats[
            "criticalChance"
        ] * damage_times_precision * (1 + stats["criticalDamages"])
        dmg_per_hour = (
            dmg_per_attack
            * stats["health"]
            / 100  # because health regen is 1/10th of total health, and one needs 10 health to make an attack
            / (1 - stats["dodge"])
            / (1 - stats["armor"])
        )
        return dmg_per_attack, dmg_per_hour

    def calc_upgrade(self, available_sp=None, cost_of_upgrade=None, stats=None):
        """
        per_hour is either 0 (dmg per attack) or 1 (dmg per hour)
        """
        if available_sp == None:
            available_sp = self.available_sp
        if cost_of_upgrade == None:
            cost_of_upgrade = deepcopy(self.cost_of_upgrade)
        dmg = self.calculate_dmg(self.stats)[self.per_hour]
        if available_sp < np.all(np.array(cost_of_upgrade.values())):
            self.convert_stats_to_percent()
            self.stats = {k: self.stats[k] - self.boni[k] for k in self.stats}
            self.convert_stats_to_proportion()
            self.stats["attack"] -= self.attack_bonus
            return dmg, self.stats
        ratios = {}
        for k in self.skill_growth.keys():
            if cost_of_upgrade[k] <= available_sp:
                self.stats[k] = self.stats[k] + self.skill_growth[k]
                if self.stats["armor"] > 0.9:
                    self.stats["armor"] = 0.9
                ratios.update(
                    {
                        k: (self.calculate_dmg(self.stats)[self.per_hour] / dmg - 1)
                        / cost_of_upgrade[
                            k
                        ]  # find the largest increase in damage per skill point
                    }
                )
                self.stats[k] = self.stats[k] - self.skill_growth[k]
            else:
                ratios.update({k: 0})
        if np.all(np.array(list(ratios.values())) <= 0):
            self.convert_stats_to_percent()
            self.stats = {k: self.stats[k] - self.boni[k] for k in self.stats}
            self.convert_stats_to_proportion()
            self.stats["attack"] -= self.attack_bonus
            return dmg, self.stats
        max_diff_key = max(ratios, key=lambda k: ratios[k])
        self.stats[max_diff_key] += self.skill_growth[max_diff_key]
        upgrade_cost = cost_of_upgrade[max_diff_key]
        cost_of_upgrade[max_diff_key] += 1
        return self.calc_upgrade(available_sp - upgrade_cost, cost_of_upgrade)

    def pull_gear_from_api(self, item_file):
        response = rq.urlopen("https://api2.warera.io/trpc/gameConfig.getGameConfig")
        txt = response.read()
        result_jsonified = json.loads(txt)
        item_data = result_jsonified["result"]["data"]["items"]
        with open(item_file, "w") as f:
            json.dump(item_data, f)


if __name__ == "__main__":
    dcalc = (
        DamageCalculator()
        .with_available_sp(0)
        .with_weaponlvl(1)
        .with_ammolvl(1)
        .with_helmetlvl(1)
        .with_chestlvl(1)
        .with_gloveslvl(1)
        .with_pantslvl(1)
        .with_bootslvl(1)
        .with_mu_hqlvl(0)
        .with_mu_orderlvl(0)
        .with_country_orderlvl(0)
        .with_country_bunkerlvl(0)
        .with_military_baselvl(0)
        .with_resistance(0)
        .with_pill(True)
        .with_ally(False)
        .with_sworn_enemy(False)
        .with_core_region(False)
        .with_attacking_region_lost(False)
        .with_region_not_linked(False)
        .with_per_hour(0)
    )
    dcalc.post_init()
    print(dcalc.boni)
    print(dcalc.calc_upgrade()[0] * 10)
