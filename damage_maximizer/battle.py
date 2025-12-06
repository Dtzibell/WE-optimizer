import numpy as np
import urllib.request as rq
import json
import re
from copy import deepcopy
import pprint
from functools import wraps
import numpy as np


class DamageCalculator:
    def __init__(
        self,
        available_sp,
        helmetlvl,
        chestlvl,
        gloveslvl,
        pantslvl,
        bootslvl,
        ammolvl,
        weaponlvl,
        mu_hqlvl,
        country_bunkerlvl,
        military_baselvl,
        country_orderlvl,
        mu_orderlvl,
        resistance,
        is_pill,
        is_core_region,
        is_ally,
        is_sworn_enemy,
        is_region_not_linked,
        is_attacking_region_lost,
        is_per_hour,
    ):
        self.is_pill_multiplier = 0.8
        self.is_core_region_multiplier = 0.15
        self.is_ally_multiplier = 0.1
        self.is_sworn_enemy_multiplier = 0.1
        self.is_region_not_linked_multiplier = -0.25
        self.is_attacking_region_lost_multiplier = -0.25

        self.available_sp = available_sp  # skill points
        self.helmetlvl = helmetlvl
        self.chestlvl = chestlvl
        self.gloveslvl = gloveslvl
        self.pantslvl = pantslvl
        self.bootslvl = bootslvl
        self.weaponlvl = weaponlvl
        self.ammolvl = ammolvl
        self.mu_hqlvl = mu_hqlvl
        self.country_bunkerlvl = country_bunkerlvl
        self.military_baselvl = military_baselvl
        self.country_orderlvl = country_orderlvl
        self.mu_orderlvl = mu_orderlvl
        self.resistance = resistance
        self.is_pill = is_pill
        self.is_core_region = is_core_region
        self.is_ally = is_ally
        self.is_sworn_enemy = is_sworn_enemy
        self.is_region_not_linked = is_region_not_linked
        self.is_attacking_region_lost = is_attacking_region_lost
        self.per_hour = is_per_hour  # calculate dmg per hour?

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
            self.weapon,
        ) = self.separate_eq()
        self.helmet["helmet0"] = {
            "dynamicStats": {
                "criticalDamages": [
                    0,
                    0,
                ]
            }
        }
        self.chest["chest0"] = {
            "dynamicStats": {
                "armor": [
                    0,
                    0,
                ]
            }
        }
        self.gloves["gloves0"] = {
            "dynamicStats": {
                "precision": [
                    0,
                    0,
                ]
            }
        }
        self.pants["pants0"] = {
            "dynamicStats": {
                "armor": [
                    0,
                    0,
                ]
            }
        }
        self.boots["boots0"] = {
            "dynamicStats": {
                "dodge": [
                    0,
                    0,
                ]
            }
        }
        self.ammo["noAmmo"] = {"flatStats": {"percentAttack": 0}}
        self.weapon["hand"] = {
            "dynamicStats": {
                "attack": [
                    0,
                    0,
                ],
                "criticalChance": [
                    0,
                    0,
                ],
            }
        }
        self.country_bunkers = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.25}
        self.military_bases = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.25}
        self.country_orders = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15}
        self.mu_orders = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15}
        self.mu_hqs = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2}

        self.weapon_hierarchy = [
            "hand",
            "knife",
            "gun",
            "rifle",
            "sniper",
            "tank",
            "jet",
        ]
        self.ammo_hierarchy = ["noAmmo", "lightAmmo", "ammo", "heavyAmmo"]

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
        clothing = ["helmet", "chest", "gloves", "pants", "boots"]
        for cloth in clothing:
            setattr(
                self,
                f"{cloth}_stats",
                getattr(self, f"{cloth}")[f"{cloth}{getattr(self, f'{cloth}lvl')}"][
                    "dynamicStats"
                ],
            )
        self.weapon_stats = self.weapon[self.weapon_hierarchy[self.weaponlvl]][
            "dynamicStats"
        ]
        self.eq_stats = [
            self.helmet_stats,
            self.chest_stats,
            self.gloves_stats,
            self.pants_stats,
            self.boots_stats,
            self.weapon_stats,
        ]
        self.bullets_stats = self.ammo[self.ammo_hierarchy[self.ammolvl]]["flatStats"]
        self.mu_hq_stats = self.mu_hqs[self.mu_hqlvl]
        self.country_bunker_stats = self.country_bunkers[self.country_bunkerlvl]
        self.military_base_stats = self.military_bases[self.military_baselvl]
        self.country_order_stats = self.country_orders[self.country_orderlvl]
        self.mu_order_stats = self.mu_orders[self.mu_orderlvl]
        self.stats = self.base_stats  # stats are in %
        self.convert_stats_to_proportion()
        self.update_boni()  # this call needs stats in proportion
        self.update_stats()

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
        helmet = {k: v for k, v in self.equipment.items() if k.startswith("helmet")}
        chest = {k: v for k, v in self.equipment.items() if k.startswith("chest")}
        gloves = {k: v for k, v in self.equipment.items() if k.startswith("gloves")}
        pants = {k: v for k, v in self.equipment.items() if k.startswith("pants")}
        boots = {k: v for k, v in self.equipment.items() if k.startswith("boots")}
        weapons = {k: v for k, v in self.equipment.items() if v["type"] == "weapon"}
        ammo = {k: v for k, v in self.equipment.items() if "ammo" in k.lower()}
        return helmet, chest, gloves, pants, boots, ammo, weapons

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

        return wrapper

    @setter
    def set_helmet_lvl(self, lvl):
        self.helmet_stats = self.helmet[f"helmet{lvl}"]["dynamicStats"]
        self.eq_stats[0] = self.helmet_stats

    @setter
    def set_chest_lvl(self, lvl):
        self.chest_stats = self.chest[f"chest{lvl}"]["dynamicStats"]
        self.eq_stats[1] = self.chest_stats

    @setter
    def set_gloves_lvl(self, lvl):
        self.gloves_stats = self.gloves[f"gloves{lvl}"]["dynamicStats"]
        self.eq_stats[2] = self.gloves_stats

    @setter
    def set_pants_lvl(self, lvl):
        self.pants_stats = self.pants[f"pants{lvl}"]["dynamicStats"]
        self.eq_stats[3] = self.pants_stats

    @setter
    def set_boots_lvl(self, lvl):
        self.boots_stats = self.boots[f"boots{lvl}"]["dynamicStats"]
        self.eq_stats[4] = self.boots_stats

    @setter
    def set_ammo_lvl(self, lvl):
        self.ammolvl = lvl
        self.bullets_stats = self.ammo[self.ammo_hierarchy[self.ammolvl]]["flatStats"]

    @setter
    def set_weapon_lvl(self, lvl):
        self.weaponlvl = lvl
        self.weapon_stats = self.weapon[self.weapon_hierarchy[self.weaponlvl]][
            "dynamicStats"
        ]
        self.eq_stats[5] = self.weapon_stats

    @setter
    def set_mu_hq_lvl(self, lvl):
        self.mu_hqlvl = lvl
        self.mu_hq_stats = self.mu_hqs[lvl]

    @setter
    def set_country_bunker_lvl(self, lvl):
        self.country_bunkerlvl = lvl
        self.country_bunker_stats = self.country_bunkers[lvl]

    @setter
    def set_military_base_lvl(self, lvl):
        self.military_baselvl = lvl
        self.military_base_stats = self.military_bases[lvl]

    @setter
    def set_country_order_lvl(self, lvl):
        self.country_orderlvl = lvl
        self.country_order_stats = self.country_orders[lvl]

    @setter
    def set_mu_order_lvl(self, lvl):
        self.mu_orderlvl = lvl
        self.mu_order_stats = self.mu_orders[lvl]

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
        self.attack_bonus = self.stats["attack"] * (
            + self.is_pill * self.is_pill_multiplier
            + self.bullets_stats["percentAttack"] / 100
        )
        self.damage_multiplier = np.sum(
            np.array(
                [
                    self.mu_hq_stats,
                    self.mu_order_stats,
                    self.country_bunker_stats,
                    self.resistance / 100,
                    self.country_order_stats,
                    self.military_base_stats,
                    self.is_core_region * self.is_core_region_multiplier,
                    self.is_ally * self.is_ally_multiplier,
                    self.is_sworn_enemy * self.is_sworn_enemy_multiplier,
                    self.is_region_not_linked * self.is_region_not_linked_multiplier,
                    self.is_attacking_region_lost
                    * self.is_attacking_region_lost_multiplier,
                ]
            )
        )
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
        for s in self.eq_stats:
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
        dmg_over_8h_cycle = (
            dmg_per_attack
            * (
                stats["health"] / 10
                + stats["health"]
                / 100  # because health regen is 1/10th of total health, and one needs 10 health to make an attack
                / (1 - stats["dodge"])
                / (1 - stats["armor"])
                * 8 
            )
        )
        return dmg_per_attack, dmg_over_8h_cycle

    def clean_up(self, dmg):
        self.convert_stats_to_percent()
        self.stats = {k: self.stats[k] - self.boni[k] for k in self.stats}
        self.convert_stats_to_proportion()
        self.stats["attack"] -= self.attack_bonus
        print(dmg, 1*self.damage_multiplier)
        return dmg * (1 + self.damage_multiplier), self.stats

    def calc_upgrade(self, available_sp=None, cost_of_upgrade=None, stats=None):
        if available_sp == None:
            available_sp = self.available_sp
        if cost_of_upgrade == None:
            cost_of_upgrade = deepcopy(self.cost_of_upgrade)

        dmg = self.calculate_dmg(self.stats)[self.per_hour]

        if available_sp < np.all(np.array(cost_of_upgrade.values())):
            return self.clean_up(dmg)

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
            return self.clean_up(dmg)

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
    dcalc = DamageCalculator(
        available_sp=0,
        helmetlvl=0,
        chestlvl=0,
        gloveslvl=0,
        pantslvl=0,
        bootslvl=0,
        ammolvl=0,
        weaponlvl=0,
        mu_hqlvl=0,
        country_bunkerlvl=0,
        military_baselvl=0,
        country_orderlvl=0,
        mu_orderlvl=0,
        resistance=0,
        is_pill=True,
        is_core_region=False,
        is_ally=False,
        is_sworn_enemy=False,
        is_region_not_linked=False,
        is_attacking_region_lost=False,
        is_per_hour=False,
    )
    print(dcalc.calc_upgrade()[0] * 1)
