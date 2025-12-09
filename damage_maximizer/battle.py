import numpy as np
import urllib.request as rq
import json
import re
from copy import deepcopy
import pprint
from functools import wraps
import numpy as np
from collections import defaultdict


class DamageCalculator:
    def __init__(
        self,
        available_sp,
        dodgelvl,
        bootslvl,
        # mu_hqlvl,
        # country_bunkerlvl,
        # military_baselvl,
        # country_orderlvl,
        # mu_orderlvl,
        # resistance,
        # is_pill,
        # is_core_region,
        # is_ally,
        # is_sworn_enemy,
        # is_region_not_linked,
        # is_attacking_region_lost,
        # is_per_hour,
    ):
        self.BASE_STATS: dict[str, float] = {
            "attack": 100,
            "precision": 50,
            "criticalChance": 10,
            "criticalDamages": 100,
            "armor": 0,
            "dodge": 0,
            "health": 50,
        }
        self.SKILL_GROWTH: dict[str, float] = {
            "attack": 20,
            "precision": 0.05,
            "criticalChance": 0.05,
            "criticalDamages": 0.2,
            "armor": 0.04,
            "dodge": 0.04,
            "health": 10,
        }
        self.WEAPON_HIERARCHY: list[str] = [
            "hand",
            "knife",
            "gun",
            "rifle",
            "sniper",
            "tank",
            "jet",
        ]
        self.AMMO_HIERARCHY: list[str] = ["noAmmo", "lightAmmo", "ammo", "heavyAmmo"]

        with open("prices.json", "r") as f:
            self.item_prices: dict[str, dict[str, dict[str, dict[str, float]]]] = (
                json.load(f)["items"]
            )
        self.item_prices.update(
            {"pill": {"pill1": {"stats": {"attack": 0.8, "price": 22}}}}
        )
        self.item_prices.update(
            {
                "ammo": {
                    "lightAmmo": {"stats": {"attack": 0.1, "price": 0.12}},
                    "ammo": {"stats": {"attack": 0.2, "price": 0.48}},
                    "heavyAmmo": {"stats": {"attack": 0.4, "price": 1.92}},
                }
            }
        )

        self.is_pill_multiplier = 0.8
        self.is_core_region_multiplier = 0.15
        self.is_ally_multiplier = 0.1
        self.is_sworn_enemy_multiplier = 0.1
        self.is_region_not_linked_multiplier = -0.25
        self.is_attacking_region_lost_multiplier = -0.25

        self.available_sp = available_sp  # skill points
        self.dodgelvl = dodgelvl

        self.bootslvl = bootslvl
        # self.mu_hqlvl = mu_hqlvl
        # self.country_bunkerlvl = country_bunkerlvl
        # self.military_baselvl = military_baselvl
        # self.country_orderlvl = country_orderlvl
        # self.mu_orderlvl = mu_orderlvl
        # self.resistance = resistance
        # self.is_pill = is_pill
        # self.is_core_region = is_core_region
        # self.is_ally = is_ally
        # self.is_sworn_enemy = is_sworn_enemy
        # self.is_region_not_linked = is_region_not_linked
        # self.is_attacking_region_lost = is_attacking_region_lost
        # self.per_hour = is_per_hour  # calculate dmg per hour?

        # self.pull_gear_from_api("items.json")
        gear = DamageCalculator.get_gear("items.json")
        equipment = self.get_equipment(gear)

        self.HELMETS = {k: v for k, v in equipment.items() if k.startswith("helmet")}
        self.CHESTS = {k: v for k, v in equipment.items() if k.startswith("chest")}
        self.GLOVES = {k: v for k, v in equipment.items() if k.startswith("gloves")}
        self.PANTS = {k: v for k, v in equipment.items() if k.startswith("pants")}
        self.BOOTS = {k: v for k, v in equipment.items() if k.startswith("boots")}
        self.WEAPONS = {k: v for k, v in equipment.items() if v["type"] == "weapon"}
        self.BULLETS = {k: v for k, v in equipment.items() if "ammo" in k.lower()}

        self.HELMETS["helmet0"] = {
            "dynamicStats": {
                "criticalDamages": [
                    0,
                    0,
                ]
            }
        }
        self.CHESTS["chest0"] = {
            "dynamicStats": {
                "armor": [
                    0,
                    0,
                ]
            }
        }
        self.GLOVES["gloves0"] = {
            "dynamicStats": {
                "precision": [
                    0,
                    0,
                ]
            }
        }
        self.PANTS["pants0"] = {
            "dynamicStats": {
                "armor": [
                    0,
                    0,
                ]
            }
        }
        self.BOOTS["boots0"] = {
            "dynamicStats": {
                "dodge": [
                    0,
                    0,
                ]
            }
        }
        self.BULLETS["noAmmo"] = {"flatStats": {"percentAttack": 0}}
        self.WEAPONS["hand"] = {
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
        self.COUNTRY_BUNKERS = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.25}
        self.MILITARY_BASES = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.25}
        self.COUNTRY_ORDERS = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15}
        self.MU_ORDERS = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15}
        self.MU_HQS = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2}

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
        self.boots_stats = self.BOOTS[f"boots{self.bootslvl}"]
        self.eq_stats = [
            self.HELMETS["helmet0"],
            # self.HELMETS["helmet1"],
            self.CHESTS["chest0"],
            self.GLOVES["gloves0"],
            self.PANTS["pants0"],
            self.boots_stats,
            self.WEAPONS[self.WEAPON_HIERARCHY[0]],
        ]
        self.gear_cost = 0
        # self.gear_cost = 2

        # self.mu_hq_stats = self.MU_HQS[self.mu_hqlvl]
        # self.country_bunker_stats = self.COUNTRY_BUNKERS[self.country_bunkerlvl]
        # self.military_base_stats = self.MILITARY_BASES[self.military_baselvl]
        # self.country_order_stats = self.COUNTRY_ORDERS[self.country_orderlvl]
        # self.mu_order_stats = self.MU_ORDERS[self.mu_orderlvl]
        self.stats = self.BASE_STATS  # stats are in %
        self.convert_stats_to_proportion()
        self.update_boni()  # this call needs stats in proportion
        self.update_stats()

    @staticmethod
    def get_gear(path: str):
        with open(path, "r") as f:
            gear = json.load(f)
        return gear

    def get_equipment(self, gear):
        c_gear = gear.copy()
        for k in gear.keys():
            if "dynamicStats" not in c_gear[k].keys() and not re.search(
                re.compile("ammo", re.IGNORECASE), k
            ):
                c_gear.pop(k)
        return gear

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
            eq = s["dynamicStats"]
            for k in eq.keys():
                self.boni[k] += (
                    eq[k][0] + (eq[k][1] - eq[k][0]) / 4
                )  # bottom quartile of the stats

        print(self.boni)

    def update_stats(self):
        print(self.stats)
        self.convert_stats_to_percent()
        self.stats: dict[str, float] = {
            k: self.BASE_STATS[k] + self.boni[k] for k in self.BASE_STATS.keys()
        }
        self.convert_stats_to_proportion()
        print(self.stats)
        # self.attack_bonus = self.stats["attack"] * (
        #     + self.is_pill * self.is_pill_multiplier
        #     + self.BULLETS_STATS["percentAttack"] / 100
        # )
        # self.damage_multiplier = np.sum(
        #     np.array(
        #         [
        #             self.mu_hq_stats,
        #             self.mu_order_stats,
        #             self.country_bunker_stats,
        #             self.resistance / 100,
        #             self.country_order_stats,
        #             self.military_base_stats,
        #             self.is_core_region * self.is_core_region_multiplier,
        #             self.is_ally * self.is_ally_multiplier,
        #             self.is_sworn_enemy * self.is_sworn_enemy_multiplier,
        #             self.is_region_not_linked * self.is_region_not_linked_multiplier,
        #             self.is_attacking_region_lost
        #             * self.is_attacking_region_lost_multiplier,
        #         ]
        #     )
        # )
        # self.stats["attack"] += self.attack_bonus

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
    def set_boots_lvl(self, lvl):
        self.boots_stats = self.BOOTS[f"boots{lvl}"]["dynamicStats"]

    @setter
    def set_dodge_lvl(self, lvl):
        self.dodgelvl = lvl

    @setter
    def set_weapon_lvl(self, lvl):
        self.weaponlvl = lvl
        self.weapon_stats = self.WEAPONS[self.WEAPON_HIERARCHY[self.weaponlvl]][
            "dynamicStats"
        ]

    @setter
    def set_mu_hq_lvl(self, lvl):
        self.mu_hqlvl = lvl
        self.mu_hq_stats = self.MU_HQS[lvl]

    @setter
    def set_country_bunker_lvl(self, lvl):
        self.country_bunkerlvl = lvl
        self.country_bunker_stats = self.COUNTRY_BUNKERS[lvl]

    @setter
    def set_military_base_lvl(self, lvl):
        self.military_baselvl = lvl
        self.military_base_stats = self.MILITARY_BASES[lvl]

    @setter
    def set_country_order_lvl(self, lvl):
        self.country_orderlvl = lvl
        self.country_order_stats = self.COUNTRY_ORDERS[lvl]

    @setter
    def set_mu_order_lvl(self, lvl):
        self.mu_orderlvl = lvl
        self.mu_order_stats = self.MU_ORDERS[lvl]

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

    def calculate_dmg_efficiency(self, stats, cost):
        ATK = stats["attack"]
        PREC = stats["precision"]
        CRATE = stats["criticalChance"]
        CDMG = stats["criticalDamages"]
        ARMOR = stats["armor"]
        DODGE = stats["dodge"]
        HEALTH = stats["health"]
        DURABILITY = 100
        COST_PER_HIT = cost / DURABILITY * (1 - stats["dodge"])
        INITIAL_HITS = HEALTH / 100
        HITS_OVER_TIME = HEALTH / 100 / (1 - DODGE) / (1 - ARMOR)
        PREC_MULTIPLIER = 0.5 * (1 + PREC)
        NORMAL_ATK = ATK * PREC_MULTIPLIER
        CRIT_ATK = ATK * PREC_MULTIPLIER * (1 + CDMG)
        DMG_PER_ATTACK = (1-CRATE) * NORMAL_ATK + CRATE * CRIT_ATK
        BTC_PER_1K_DMG = COST_PER_HIT / DMG_PER_ATTACK * 1000 
        DMG_OVER_8H = DMG_PER_ATTACK * INITIAL_HITS * HITS_OVER_TIME
        return DMG_OVER_8H, BTC_PER_1K_DMG

    def clean_up(self, dmg):
        self.convert_stats_to_percent()
        self.stats = {k: self.stats[k] - self.boni[k] for k in self.stats}
        self.convert_stats_to_proportion()
        self.stats["attack"] -= self.attack_bonus
        return dmg * (1 + self.damage_multiplier), self.stats

    def calc_upgrade(self, available_sp=None, cost_of_upgrade=None):
        if available_sp == None:
            available_sp = self.available_sp
        if cost_of_upgrade == None:
            cost_of_upgrade = deepcopy(self.cost_of_upgrade)

        BASE_EFFICIENCY = self.calculate_dmg_efficiency(self.stats, self.gear_cost)

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
        available_sp=52,
        bootslvl=0,
        dodgelvl=0,
        # mu_hqlvl=0,
        # couuntry_bunkerlvl=0,
        # miulitary_baselvl=0,
        # couuntry_orderlvl=0,
        # muu_orderlvl=0,
        # reusistance=0,
        # isu_pill=False,
        # isu_core_region=False,
        # isu_ally=False,
        # isu_sworn_enemy=False,
        # isu_region_not_linked=False,
        # isu_attacking_region_lost=False,
        # isu_per_hour=False,
    )
