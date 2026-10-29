import random
TAX = 0.25
DEP = 1_200_000 // 4
worst_identity = 0.0
worst_shield = 0.0
fails = 0
rng = random.Random(1)
for seed in range(20000):
    rng = random.Random(seed)
    for _ in range(4):
        rev = rng.randrange(50, 71) * 10_000
        cost = rng.randrange(20, 31) * 10_000
        ebitda = rev - cost
        ebit = ebitda - DEP
        tax = TAX * ebit
        ocf = ebit - tax + DEP
        shield = TAX * DEP
        d1 = abs(ocf - (ebitda * (1 - TAX) + shield))
        ocf_without = ebitda - TAX * ebitda
        d2 = abs((ocf - ocf_without) - DEP * TAX)
        worst_identity = max(worst_identity, d1)
        worst_shield = max(worst_shield, d2)
        if not (d1 < 1e-6 and d2 < 1e-6):
            fails += 1
print("pairs checked: 80000; worst identity deviation (cents):", worst_identity, "; worst shield deviation:", worst_shield, "; failures:", fails)
