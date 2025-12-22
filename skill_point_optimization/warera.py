# entre = [30 + i for i in range(0,100,5)]
# ener = [30 + i for i in range(0,100,10)]
# entre_actions_per_day = [i*24/100 for i in entre]
# ener_actions_per_day = [i*24/100 for i in ener]
# entre_actions_per_sp = [0.]
# entre_actions_per_sp.extend([1.2/i for i in range(1,20)])
# ener_actions_per_sp = [0.]
# ener_actions_per_sp.extend([2.4/i for i in range(1,20)])
# production = [10 + i for i in range(0,100,3)]
# prod_ratio = [0.]
# prod_ratio.extend([production[i+1] / production[i] - 1 for i in range(0,20)])
# 
# sum = 14.4
# sp = 100
# entre_ind = 1
# ener_ind = 1
# prod_ind = 1
# prod_rate = 1
# prods = []
# upgrades = []
# while sp >= 0:
#     if (1 + prod_ratio[prod_ind]/ prod_ind) * sum  > sum + 2.4 / ener_ind and (1 + prod_ratio[prod_ind]/ prod_ind) * sum  > sum + 1.2 / entre_ind and sp - prod_ind >= 0 and prod_ind < 10:
#         sum *= 1+prod_ratio[prod_ind]
#         prod_rate += prod_ratio[prod_ind]
#         sp -= prod_ind
#         prod_ind += 1
#         upgrades.append("prod")
#     elif entre_actions_per_sp[entre_ind] > ener_actions_per_sp[ener_ind] and sp - entre_ind >= 0 and entre_ind < 10:
#         sum += 1.2*prod_rate
#         sp -= entre_ind
#         entre_ind += 1
#         upgrades.append("entre")
#     elif sp - ener_ind >= 0 and ener_ind < 10:
#         sum += 2.4*prod_rate
#         sp -= ener_ind
#         ener_ind+=1
#         upgrades.append("ener")
#     else:
#         break
# print(sp)
# print(f"prod: {prod_ind}")
# print(f"entre: {entre_ind}")
# print(f"ener: {ener_ind}")

# ppp = 0.0615 # price per production point
# companies_p_lvl = 24 # production per day
# companies_lvl = 11
# companiesprod = companies_lvl * companies_p_lvl
# time = 0
# for j in [50 + a for a in range(50, 551, 50)]:
#     for i in range(0,400):
#         upgrades1 = [i, j, 20, 40, i]
#         upgrades2 = [j, 20, 40, i, i]
#         time1, time2 = 0, 0
#         money_p_day = companiesprod * ppp
#         for u in upgrades1:
#             time1 += u / money_p_day
#             money_p_day += 24 * ppp
#         money_p_day = companiesprod * ppp
#         for u in upgrades2:
#             time2 += u / money_p_day
#             money_p_day += 24*ppp
#         if time1 > time2:
#             print(j, i/j)
#             break

PROD_SKILL = 10
ENTRE_SKILL = 30
ENER_SKILL = 30
COMPANIES_LVL = 15
PROD_BONUS = 1.395
ppp = 0.0615 # price per production point
companiesprod = COMPANIES_LVL * PROD_BONUS
entre = ENTRE_SKILL / 100
ener = ENER_SKILL / 100
prod = 31 * 1.395
skills_prod = (entre+ener) * prod
sum = ((entre + ener) * prod + companiesprod) * 24
print(sum*ppp)
