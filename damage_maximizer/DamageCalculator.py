import numpy as np
import json
from copy import deepcopy
from pprint import pp
import numpy as np

class DamageCalculator:
    def __init__(
        self,
        available_sp,
        available_btc,
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


        self.is_core_region_multiplier = 0.15
        self.is_ally_multiplier = 0.1
        self.is_sworn_enemy_multiplier = 0.1
        self.is_region_not_linked_multiplier = -0.25
        self.is_attacking_region_lost_multiplier = -0.25

        self.available_sp = available_sp
        self.available_btc = available_btc
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
        
        self.COUNTRY_BUNKERS = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.25}
        self.MILITARY_BASES = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2, 5: 0.25}
        self.COUNTRY_ORDERS = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15}
        self.MU_ORDERS = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15}
        self.MU_HQS = {0: 0, 1: 0.05, 2: 0.1, 3: 0.15, 4: 0.2}


        # self.mu_hq_stats = self.MU_HQS[self.mu_hqlvl]
        # self.country_bunker_stats = self.COUNTRY_BUNKERS[self.country_bunkerlvl]
        # self.military_base_stats = self.MILITARY_BASES[self.military_baselvl]
        # self.country_order_stats = self.COUNTRY_ORDERS[self.country_orderlvl]
        # self.mu_order_stats = self.MU_ORDERS[self.mu_orderlvl]

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



    def calc_upgrade(self, available_sp=None, cost_of_upgrade=None):
        if available_sp == None:
            available_sp = self.available_sp
        if cost_of_upgrade == None:
            cost_of_upgrade = deepcopy(self.cost_of_upgrade)
        if np.all(np.array(cost_of_upgrade.values()) < available_sp):
            return self.stats, self.get_dmg_eff() # potentially returns modified stats

        BASE_EFFICIENCY = self.get_dmg_eff()
        ratios = {}
        for k in self.SKILL_GROWTH.keys():
            if cost_of_upgrade[k] <= available_sp:
                self.stats[k] = self.stats[k] + self.SKILL_GROWTH[k]
                if self.stats["armor"] > 0.9:
                    self.stats["armor"] = 0.9
                ratios.update(
                    {
                        k: (self.get_dmg_eff() - BASE_EFFICIENCY)
                        / cost_of_upgrade[
                            k
                        ]  # find the largest increase in damage per skill point
                    }
                )
                self.stats[k] = self.stats[k] - self.SKILL_GROWTH[k]
            else:
                ratios.update({k: 0})

        max_diff_key = max(ratios, key=lambda k: ratios[k])
        self.stats[max_diff_key] += self.SKILL_GROWTH[max_diff_key]
        upgrade_cost = cost_of_upgrade[max_diff_key]
        cost_of_upgrade[max_diff_key] += 1
        return self.calc_upgrade(available_sp - upgrade_cost, cost_of_upgrade)
    
    def get_optimal_build(self):
        BASE_EFFICIENCY = self.get_dmg_eff()
        # for each item in knives, helmet1... in self.item_prices

if __name__ == "__main__":
    dcalc = DamageCalculator(
        available_sp=52,
        available_btc=100,
        # mu_hqlvl=0,
        # country_bunkerlvl=0,
        # military_baselvl=0,
        # country_orderlvl=0,
        # mu_orderlvl=0,
        # resistance=0,
        # is_pill=False,
        # is_core_region=False,
        # is_ally=False,
        # is_sworn_enemy=False,
        # is_region_not_linked=False,
        # is_attacking_region_lost=False,
        # is_per_hour=False,
    )
    print(dcalc.item_prices)
