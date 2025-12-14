import json
from os import stat
import re
import sys
import urllib.request as rq
from functools import wraps
from copy import deepcopy
import numpy as np
from pprint import pp


class Stats:
    def __init__(
        self,
        available_skill_points,
        available_BTC,
    ):
        self.skill_boni = {
            "attack": 0.0,
            "precision": 0.0,
            "criticalChance": 0.0,
            "criticalDamages": 0.0,
            "armor": 0.0,
            "dodge": 0.0,
            "health": 0.0,
        }
        self.AVAILABLE_SKILL_POINTS = available_skill_points
        self.AVAILABLE_BTC = available_BTC
        self.BASE_STATS: dict[str, float] = {
            "attack": 100,
            "precision": 50,
            "criticalChance": 10,
            "criticalDamages": 100,
            "armor": 0,
            "dodge": 0,
            "health": 50,
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

        self.is_pill_multiplier = 0
        self.helmet = {"criticalDamages": 0}
        self.chest = {"armor": 0}
        self.gloves = {"precision": 0}
        self.pants = {"armor": 0}
        self.boots = {"dodge": 0}
        self.weapon = {"attack": 0, "criticalChance": 0}
        self.bullets = {"percentAttack": 0}
        self.eq_boni = {
            "attack": 0,
            "precision": 0,
            "criticalChance": 0,
            "criticalDamages": 0,
            "armor": 0,
            "dodge": 0,
            "health": 0,
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
        self.SKILL_GROWTH: dict[str, float] = {
            "attack": 20,
            "precision": 0.05,
            "criticalChance": 0.05,
            "criticalDamages": 0.2,
            "armor": 0.04,
            "dodge": 0.04,
            "health": 10,
        }

        self.gear_cost = 0
        with open("prices.json", "r") as f:
            self.item_prices = json.load(f)["items"]

        self.item_prices.update({"pill": {True: {"attack": 0.8, "price": 22}}})
        self.item_prices.update(
            {
                "bullets": {
                    0: {"attack": 0.0, "price": 0.0},
                    0.1: {"attack": 0.1, "price": 0.12},
                    0.2: {"attack": 0.2, "price": 0.48},
                    0.4: {"attack": 0.4, "price": 1.92},
                }
            }
        )

        self.pill_price = 0
        self.bullet_price = 0

    def update_eq_boni(self):
        self.eq_boni = {
            "attack": 0,
            "precision": 0,
            "criticalChance": 0,
            "criticalDamages": 0,
            "armor": 0,
            "dodge": 0,
            "health": 0,
        }
        eq_boni = [
            self.helmet,
            self.chest,
            self.gloves,
            self.pants,
            self.boots,
            self.weapon,
        ]
        for eq in eq_boni:
            for k in eq:
                self.eq_boni[k] += eq[k]

    @staticmethod
    def setter(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.update_eq_boni()
            self.update_stats()

        return wrapper

    @setter
    def set_helmet(self, cdmg):
        stat = "criticalDamages"
        self.helmet[stat] = cdmg

    @setter
    def set_chest(self, armor):
        stat = "armor"
        self.chest[stat] = armor

    @setter
    def set_gloves(self, prec):
        stat = "precision"
        self.gloves[stat] = prec

    @setter
    def set_pants(self, armor):
        stat = "armor"
        self.pants[stat] = armor

    @setter
    def set_boots(self, dodge):
        stat = "dodge"
        self.boots[stat] = dodge

    @setter
    def set_weapon(self, att, crate):
        stat1 = "attack"
        stat2 = "criticalChance"
        self.weapon[stat1] = att
        self.weapon[stat2] = crate

    @setter
    def set_bullets(self, patt):
        self.bullets["percentAttack"] = patt
        self.bullet_price = self.item_prices["bullets"][patt]["price"]

    @setter
    def set_pill(self, is_pill):
        if is_pill:
            self.is_pill_multiplier = 0.80
            self.pill_price = self.item_prices["pill"][True]["price"]
        else:
            self.is_pill_multiplier = 0
            self.pill_price = 0

    def update_stats(self):
        self.stats = deepcopy(self.BASE_STATS)
        self.convert_stats_to_proportion()
        self.stats = {
            k: self.stats[k] + self.skill_boni[k] for k in self.stats
        }
        self.stats["attack"] *= (
            1 + self.is_pill_multiplier + self.bullets["percentAttack"]
        )
        self.convert_stats_to_percent()
        self.stats = {
            k: self.stats[k] + self.eq_boni[k] for k in self.BASE_STATS.keys()
        }

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

    def get_dmg_8h(self):
        self.convert_stats_to_proportion()
        ATK = self.stats["attack"]
        PREC = self.stats["precision"]
        CRATE = self.stats["criticalChance"]
        CDMG = self.stats["criticalDamages"]
        ARMOR = self.stats["armor"]
        DODGE = self.stats["dodge"]
        HEALTH = self.stats["health"]
        INITIAL_HITS = HEALTH / 10
        HITS_OVER_TIME = HEALTH / 100 / (1 - DODGE) / (1 - ARMOR) * 8
        PREC_MULTIPLIER = 0.5 * (1 + PREC)
        NORMAL_ATK = ATK * PREC_MULTIPLIER
        CRIT_ATK = ATK * PREC_MULTIPLIER * (1 + CDMG)
        DMG_PER_HIT = (1 - CRATE) * NORMAL_ATK + CRATE * CRIT_ATK
        DMG_OVER_8H = DMG_PER_HIT * (INITIAL_HITS + HITS_OVER_TIME)
        self.convert_stats_to_percent()
        return DMG_OVER_8H, INITIAL_HITS + HITS_OVER_TIME

    def get_dmg_eff(self):
        DODGE = self.stats["dodge"] / 100
        DMG_WITH_GEAR, TOTAL_HITS = self.get_dmg_8h()
        TOTAL_EQ_DEPREC = (
            self.gear_cost / 100 / (1 - DODGE) * TOTAL_HITS
            + self.pill_price
            + self.bullet_price * TOTAL_HITS
        )
        self.stats = {k: self.stats[k] - self.eq_boni[k] for k in self.stats.keys()}
        self.stats["attack"] /= (
            1 + self.is_pill_multiplier + self.bullets["percentAttack"]
        )

        DMG_WITHOUT_GEAR, _ = self.get_dmg_8h()
        DMG_RATIO = DMG_WITH_GEAR / DMG_WITHOUT_GEAR
              #dmg eff: {DMG_EFF}
        # print(f"""
        #       dmg ratio: {DMG_RATIO}
        #       DMG_WITHOUT_GEAR: {DMG_WITHOUT_GEAR}
        #       DMG_WITH_GEAR: {DMG_WITH_GEAR}
        #       dmg diff: {DMG_DIFF}
        #       total hits: {TOTAL_HITS}
        #       eq deprec: {TOTAL_EQ_DEPREC}
        #       gear cost: {self.gear_cost}
        #       """)
        DMG_EFF = (DMG_RATIO - 1) / (TOTAL_EQ_DEPREC * TOTAL_HITS)
        self.stats = {k: self.stats[k] + self.eq_boni[k] for k in self.stats.keys()}
        return DMG_EFF

    def calc_skill_points(
        self, available_sp=None, cost_of_upgrade=None, skill_boni=None
    ):
        if available_sp == None:
            available_sp = self.AVAILABLE_SKILL_POINTS
        if cost_of_upgrade == None:
            cost_of_upgrade = deepcopy(self.cost_of_upgrade)
        if skill_boni == None:
            self.skill_boni = {
                "attack": 0.0,
                "precision": 0.0,
                "criticalChance": 0.0,
                "criticalDamages": 0.0,
                "armor": 0.0,
                "dodge": 0.0,
                "health": 0.0,
            }
        if np.all(np.array(list(cost_of_upgrade.values())) > available_sp):
            return self.skill_boni
        BASE_EFFICIENCY = self.get_dmg_eff()
        ratios = {}
        for k in self.SKILL_GROWTH.keys():
            if cost_of_upgrade[k] <= available_sp:
                self.skill_boni[k] += self.SKILL_GROWTH[k]
                if self.skill_boni["armor"] > 0.9:
                    self.skill_boni["armor"] = 0.9
                self.update_stats()
                ratios.update(
                    {k: (self.get_dmg_eff() - BASE_EFFICIENCY) / cost_of_upgrade[k]}
                )
                self.skill_boni[k] -= self.SKILL_GROWTH[k]
            else:
                ratios.update({k: 0})
        max_diff_key = max(ratios, key=lambda k: ratios[k])
        self.skill_boni[max_diff_key] += self.SKILL_GROWTH[max_diff_key]
        self.update_stats()
        upgrade_cost = cost_of_upgrade[max_diff_key]
        cost_of_upgrade[max_diff_key] += 1
        return self.calc_skill_points(
            available_sp - upgrade_cost, cost_of_upgrade, self.skill_boni
        )

    def apply_skill_points(self, eff_upgrades=None, available_btc = None):
        most_eff_upgrade = ("", "", 0)  # item type, item key, efficiency
        if eff_upgrades == None:
            eff_upgrades = {
                    "helmet": ("", "", 0,0),
                    "chest": ("", "", 0,0),
                    "gloves": ("", "", 0,0),
                    "pants": ("", "", 0,0),
                    "boots": ("", "", 0,0),
                    "weapon": ("", "", 0,0),
                    "bullets": ("", "", 0,0),
                    "pill": ("", "", 0,0),
                    }
        if available_btc == None:
            available_btc = self.AVAILABLE_BTC
        if self.gear_cost > available_btc:
            print(self.gear_cost)
            print(eff_upgrades)
            return eff_upgrades
        for item_type, item_stats in self.item_prices.items():
            match item_type:
                case "weapon":
                    for key, stat in item_stats.items():
                        self.set_weapon(
                            att=stat["attack"], crate=stat["criticalChance"]
                        )
                        self.gear_cost -= eff_upgrades["weapon"][3]
                        self.gear_cost += stat["price"]
                        self.calc_skill_points()
                        dmg_eff = self.get_dmg_eff()
                        self.set_weapon(att=0, crate=0)
                        self.gear_cost -= stat["price"]
                        self.gear_cost += eff_upgrades["weapon"][3]
                        if dmg_eff > most_eff_upgrade[2]:
                            most_eff_upgrade = (item_type, key, dmg_eff, stat["price"])
                case "pill":
                    for key, stat in item_stats.items():
                        self.set_pill(True)
                        self.calc_skill_points()
                        dmg_eff = self.get_dmg_eff()
                        self.set_pill(False)
                        if dmg_eff > most_eff_upgrade[2]:
                            most_eff_upgrade = (item_type, key, dmg_eff, stat["price"])
                case "helmet":
                    for key, stat in item_stats.items():
                        self.set_helmet(cdmg=stat["criticalDamages"])
                        self.gear_cost -= eff_upgrades["helmet"][3]
                        self.gear_cost += stat["price"]
                        self.calc_skill_points()
                        dmg_eff = self.get_dmg_eff()
                        self.set_helmet(cdmg=0)
                        self.gear_cost -= stat["price"]
                        self.gear_cost += eff_upgrades["helmet"][3]
                        if dmg_eff > most_eff_upgrade[2]:
                            most_eff_upgrade = (item_type, key, dmg_eff, stat["price"])
                case "chest":
                    for key, stat in item_stats.items():
                        self.set_chest(armor=stat["armor"])
                        self.gear_cost -= eff_upgrades["chest"][3]
                        self.gear_cost += stat["price"]
                        self.calc_skill_points()
                        dmg_eff = self.get_dmg_eff()
                        self.set_chest(armor=0)
                        self.gear_cost -= stat["price"]
                        self.gear_cost += eff_upgrades["chest"][3]
                        if dmg_eff > most_eff_upgrade[2]:
                            most_eff_upgrade = (item_type, key, dmg_eff, stat["price"])
                case "gloves":
                    for key, stat in item_stats.items():
                        self.set_gloves(prec=stat["precision"])
                        self.gear_cost -= eff_upgrades["gloves"][3]
                        self.gear_cost += stat["price"]
                        self.calc_skill_points()
                        dmg_eff = self.get_dmg_eff()
                        self.set_gloves(prec=0)
                        self.gear_cost -= stat["price"]
                        self.gear_cost += eff_upgrades["gloves"][3]
                        if dmg_eff > most_eff_upgrade[2]:
                            most_eff_upgrade = (item_type, key, dmg_eff, stat["price"])
                case "pants":
                    for key, stat in item_stats.items():
                        self.set_pants(armor=stat["armor"])
                        self.gear_cost -= eff_upgrades["pants"][3]
                        self.gear_cost += stat["price"]
                        self.calc_skill_points()
                        dmg_eff = self.get_dmg_eff()
                        self.set_pants(armor=0)
                        self.gear_cost -= stat["price"]
                        self.gear_cost += eff_upgrades["pants"][3]
                        if dmg_eff > most_eff_upgrade[2]:
                            most_eff_upgrade = (item_type, key, dmg_eff, stat["price"])
                case "boots":
                    for key, stat in item_stats.items():
                        self.set_boots(dodge=stat["dodge"])
                        self.gear_cost -= eff_upgrades["boots"][3]
                        self.gear_cost += stat["price"]
                        self.calc_skill_points()
                        dmg_eff = self.get_dmg_eff()
                        self.set_boots(dodge=0)
                        self.gear_cost -= stat["price"]
                        self.gear_cost += eff_upgrades["boots"][3]
                        if dmg_eff > most_eff_upgrade[2]:
                            most_eff_upgrade = (item_type, key, dmg_eff, stat["price"])
                case "bullets":
                    for key, stat in item_stats.items():
                        if key == 0:
                            continue
                        self.set_bullets(patt=stat["attack"])
                        # self.gear_cost += stat["price"]
                        self.calc_skill_points()
                        dmg_eff = self.get_dmg_eff()
                        self.set_bullets(patt=0)
                        if dmg_eff > most_eff_upgrade[2]:
                            most_eff_upgrade = (item_type, key, dmg_eff, stat["price"])
        if most_eff_upgrade == ("", "", 0):
            print(eff_upgrades)
            return 
        if eff_upgrades[most_eff_upgrade[0]][2] < most_eff_upgrade[2]:
            self.gear_cost -= eff_upgrades[most_eff_upgrade[0]][3]
            eff_upgrades[most_eff_upgrade[0]] = most_eff_upgrade
            self.gear_cost += most_eff_upgrade[3]
        if most_eff_upgrade[0] == "weapon":
            stats = most_eff_upgrade[1].split(",")
            attack = int(stats[0])
            crate = int(stats[1])
            getattr(self, f"set_{most_eff_upgrade[0]}")(attack, crate)
        else:
            getattr(self, f"set_{most_eff_upgrade[0]}")(int(most_eff_upgrade[1]))
        del self.item_prices[most_eff_upgrade[0]][most_eff_upgrade[1]]
        if most_eff_upgrade[0] not in ["pill", "bullets"]:
            print(self.gear_cost)
        return self.apply_skill_points(eff_upgrades, available_btc)


# {'weapon': {'21, 21': {'attack': 21, 'criticalChance': 21, 'price': 571.65},
#             '21, 29': {'attack': 21, 'criticalChance': 29, 'price': 576.8},
#             '21, 33': {'attack': 21, 'criticalChance': 33, 'price': 587.1},
#             '22, 29': {'attack': 22, 'criticalChance': 29, 'price': 587.1},
#             '22, 27': {'attack': 22, 'criticalChance': 27, 'price': 597.4},
#             '20, 30': {'attack': 20, 'criticalChance': 30, 'price': 616.97},
#             '21, 30': {'attack': 21, 'criticalChance': 30, 'price': 618.0},
#             '24, 28': {'attack': 24, 'criticalChance': 28, 'price': 618.0},
#             '23, 34': {'attack': 23, 'criticalChance': 34, 'price': 638.6},
#             '27, 29': {'attack': 27, 'criticalChance': 29, 'price': 661.26},
#             '27, 23': {'attack': 27, 'criticalChance': 23, 'price': 721.0},
#             '28, 30': {'attack': 28, 'criticalChance': 30, 'price': 721.0}},
#  'helmet': {'74': {'criticalDamages': 74, 'price': 560.32},
#             '78': {'criticalDamages': 78, 'price': 721.0}},
#  'chest': {'34': {'armor': 34, 'price': 509.85},
#            '38': {'armor': 38, 'price': 618.0}},
#  'gloves': {'39': {'precision': 39, 'price': 611.881}},
#  'pants': {'34': {'armor': 34, 'price': 463.5},
#            '37': {'armor': 37, 'price': 509.85},
#            '40': {'armor': 40, 'price': 978.5}},
#  'boots': {'32': {'dodge': 32, 'price': 486.16},
#            '33': {'dodge': 33, 'price': 488.22},
#            '37': {'dodge': 37, 'price': 566.5},
#            '38': {'dodge': 38, 'price': 616.97},
#            '39': {'dodge': 39, 'price': 746.75}},
#  'pill': {'0.8': {'attack': 0.8, 'price': 22}},
#  'ammo': {'0.1': {'attack': 0.1, 'price': 0.12},
#           '0.2': {'attack': 0.2, 'price': 0.48},
#           '0.4': {'attack': 0.4, 'price': 1.92}}}

stats = Stats(
    available_skill_points=52,
    available_BTC=1000,
)
# stats.set_helmet(15)
# stats.set_weapons(20, 10)
# stats.set_pill(True)
stats.apply_skill_points()
print(stats.stats)
print(stats.calc_skill_points())
print(stats.get_dmg_8h())
