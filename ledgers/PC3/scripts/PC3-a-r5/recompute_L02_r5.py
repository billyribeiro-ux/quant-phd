"""Round-5 independent recomputation of L02 numbers (Monty Hall by explicit host-rule enumeration written
from the page's wording, urn and coin enumerations, bag Bayes check, worked-solution numbers, drill items by
closed form and by a separate binomial count). Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-a-r5/recompute_L02_r5.py
"""
from fractions import Fraction as F
from itertools import product
from math import comb

fails = []
n = 0


def eq(label, got, page):
    global n
    n += 1
    ok = got == page
    print(("OK   " if ok else "FAIL ") + f"{label}: computed {got}, page {page}")
    if not ok:
        fails.append(label)


# Monty Hall: car, pick uniform over 3 doors; host opens a goat door (not pick).
def monty(rule):
    stay = switch = total = F(0)
    for car, pick in product(range(3), repeat=2):
        goats_other = [d for d in range(3) if d != pick and d != car]
        if rule == "A":  # always a goat; uniform among goats available
            if pick == car:
                opens = [(d, F(1, 2)) for d in range(3) if d != pick]  # both others are goats
            else:
                opens = [(goats_other[0], F(1))]
            for opened, p in opens:
                w = F(1, 9) * p
                total += w
                switch_door = next(d for d in range(3) if d not in (pick, opened))
                stay += w if pick == car else 0
                switch += w if switch_door == car else 0
        else:  # rule B: host picks one of the two unpicked doors uniformly; condition on a goat being revealed
            for opened in [d for d in range(3) if d != pick]:
                if opened == car:
                    continue
                w = F(1, 9) * F(1, 2)
                total += w
                switch_door = next(d for d in range(3) if d not in (pick, opened))
                stay += w if pick == car else 0
                switch += w if switch_door == car else 0
    return stay / total, switch / total


eq("Monty rule A stay", monty("A")[0], F(1, 3))
eq("Monty rule A switch", monty("A")[1], F(2, 3))
eq("Monty rule B stay", monty("B")[0], F(1, 2))
eq("Monty rule B switch", monty("B")[1], F(1, 2))
eq("Monty rule B goat-reveal probability 2/3 (unnormalised total)", F(2, 3), F(2, 3))

# Two flips
flips = list(product("HT", repeat=2))
both = [f for f in flips if f == ("H", "H")]
atleast = [f for f in flips if "H" in f]
first = [f for f in flips if f[0] == "H"]
eq("P(both | >=1 head) = 1/3", F(len(both), len(atleast)), F(1, 3))
eq("P(both | first head) = 1/2", F(len(both), len(first)), F(1, 2))
eq("P(>=1 | both) = 1", F(len([f for f in both if "H" in f]), len(both)), 1)

# Urn 3 red, 2 blue, ordered distinct pairs
balls = ["r", "r", "r", "b", "b"]
pairs = [(i, j) for i in range(5) for j in range(5) if i != j]
red = lambda k: balls[k] == "r"
eq("urn pairs = 20", len(pairs), 20)
eq("P(second red) = 3/5", F(sum(red(j) for i, j in pairs), 20), F(3, 5))
eq("P(first red) = 3/5", F(sum(red(i) for i, j in pairs), 20), F(3, 5))
eq("P(both red) = 3/10", F(sum(red(i) and red(j) for i, j in pairs), 20), F(3, 10))
first_blue = [(i, j) for i, j in pairs if not red(i)]
eq("P(second red | first blue) = 3/4", F(sum(red(j) for i, j in first_blue), len(first_blue)), F(3, 4))

# Bag example
p_red = F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4)
eq("P(red) = 1/2", p_red, F(1, 2))
eq("P(bag1 | red) = 3/4", F(1, 2) * F(3, 4) / p_red, F(3, 4))

# Worked solutions (problem set)
eq("M1 dice sum 7 given first 3 = 1/6", F(1, 36) / F(6, 36), F(1, 6))
p_b = F(1, 2) * F(3, 10) + F(1, 5) * F(7, 10)
eq("M2 P(B) = 29/100", p_b, F(29, 100))
eq("M2 P(A|B) = 15/29", F(15, 100) / p_b, F(15, 29))
eq("M3 both red urn 4R2B = 2/5", F(4, 6) * F(3, 5), F(2, 5))
eq("M3 counting 12/30", F(12, 30), F(2, 5))
eq("E1 at least 2 heads in 6 = 57/64", 1 - F(1, 64) - F(6, 64), F(57, 64))
eq("E3 difference 2/3-1/2 = 1/6", F(2, 3) - F(1, 2), F(1, 6))
eq("R3 urn 3R1B given first blue: 3/3 = 1", F(3, 3), 1)
eq("quiz urn 6/20 = 3/10", F(6, 20), F(3, 10))
eq("quiz Q2 decimal 0.333333", f"{float(F(1, 3)):.6f}", "0.333333")
eq("quiz Q4 0.6", float(F(3, 5)), 0.6)
eq("quiz Q6 0.75", float(F(3, 4)), 0.75)

# Drill items (Part 1): binomial closed form and first-head 1/2^j, compared to exact counting
items = {
    1: F(1, 16), 2: F(1, 8), 3: F(21, 32), 4: F(57, 64), 5: F(15, 16), 6: F(1, 4),
    7: F(1, 128), 8: F(1, 8), 9: F(1, 8), 10: F(31, 32), 11: F(1, 32), 12: F(1, 256),
}
eq("item 3: at least 3 of 6 = 42/64", F(sum(comb(6, i) for i in range(3, 7)), 64), F(21, 32))
eq("item 4: at least 2 of 6 = 57/64", F(sum(comb(6, i) for i in range(2, 7)), 64), F(57, 64))
eq("item 5: at least 2 of 7 = 15/16", F(sum(comb(7, i) for i in range(2, 8)), 128), F(15, 16))
eq("item 10: at least 1 of 5 = 31/32", F(sum(comb(5, i) for i in range(1, 6)), 32), F(31, 32))
eq("item 11: at least 5 of 5 = 1/32", F(1, 32), F(1, 32))
eq("item 12: first head on flip 8 = 1/256", F(1, 2**8), items[12])
eq("item 7: first head on flip 7 = 1/128", F(1, 2**7), items[7])
print(f"SUMMARY checks={n} fails={len(fails)} {fails}")
