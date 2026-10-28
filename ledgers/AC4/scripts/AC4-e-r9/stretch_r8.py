"""Re-derive the two Rung 4 stretch claims (project.html lines 398-399) with exact rationals on random cases.

Sign convention: favourable positive. Sales price, volume and mix as on the page; efficiency per input at its standard
price; input price variance (s - a) times actual input units; fixed overhead variance budget less actual.
"""
import random
from fractions import Fraction as F

random.seed(8)
spend_bad = two_bad = two_gap_bad = 0
n_two = n_gap = n_spend = 0
N = 3000
for _ in range(N):
    nprod = random.randint(1, 3)
    ninp = random.choice([1, 2])
    s = [random.randint(1, 300) for _ in range(ninp)]
    a = [s[k] if random.random() < 0.3 else random.randint(1, 300) for k in range(ninp)]
    prods = []
    for _ in range(nprod):
        prods.append(dict(bu=random.randint(0, 50), bp=random.randint(0, 5000), q=[random.randint(0, 5) for _ in range(ninp)],
                          au=random.randint(0, 50), ap=random.randint(0, 5000)))
    if sum(p["bu"] for p in prods) == 0:
        prods[0]["bu"] = 1
    F_b = random.randint(0, 20000)
    F_a = F_b if random.random() < 0.5 else random.randint(0, 20000)
    AQ = [random.randint(0, 200) for _ in range(ninp)]
    BU = sum(p["bu"] for p in prods); AU = sum(p["au"] for p in prods)
    cm = [p["bp"] - sum(p["q"][k] * s[k] for k in range(ninp)) for p in prods]
    master = sum(p["bu"] * c for p, c in zip(prods, cm)) - F_b
    rev_b = sum(p["bu"] * p["bp"] for p in prods)
    var_b = sum(p["bu"] * sum(p["q"][k] * s[k] for k in range(ninp)) for p in prods)
    flex = F(AU) * (F(rev_b, BU) - F(var_b, BU)) - F_b          # exact flexed profit (no page rounding needed for identity)
    price = sum((p["ap"] - p["bp"]) * p["au"] for p in prods)
    volume = flex - master
    mix = sum(p["au"] * c for p, c in zip(prods, cm)) - F_b - flex
    eff = [s[k] * (sum(p["q"][k] * p["au"] for p in prods) - AQ[k]) for k in range(ninp)]
    actual_profit = sum(p["au"] * p["ap"] for p in prods) - sum(a[k] * AQ[k] for k in range(ninp)) - F_a
    total = actual_profit - master
    ipv = [(s[k] - a[k]) * AQ[k] for k in range(ninp)]
    fov = F_b - F_a
    # two-input claim: five figures (price, volume, mix, two efficiency) add to the total when a = s
    if ninp == 2 and F_a == F_b and all(a[k] == s[k] for k in range(ninp)):
        n_two += 1
        if price + volume + mix + sum(eff) != total:
            two_bad += 1
    # general gap: total minus those five equals the sum of the input price variances
    if ninp == 2 and F_a == F_b:
        n_gap += 1
    if ninp == 2 and F_a == F_b and total - (price + volume + mix + sum(eff)) != sum(ipv):
        two_gap_bad += 1
    # spending claim: six figures (one input, a single s) add to the total whatever a is
    if ninp == 1:
        n_spend += 1
    if ninp == 1 and price + volume + mix + eff[0] + ipv[0] + fov != total:
        spend_bad += 1
print("spending cases (one input)", sum(1 for _ in range(0)))
print("counts: two-input a=s,F_a=F_b", n_two, "gap cases", n_gap, "one-input spending cases", n_spend)
print("cases", N, "two-input (a=s) mismatches", two_bad, "gap identity mismatches", two_gap_bad, "spending six-figure mismatches", spend_bad)
# witness from the Round-7 FAIL row: input 1 price 50 vs actual 60, 200 units; input 2 at standard
ps = [dict(bu=100, bp=1000, q=[2, 1], au=100, ap=1000)]
s = [50, 200]; a = [60, 200]; AQ = [200, 100]; F_b = F_a = 0
cm = [p["bp"] - sum(p["q"][k] * s[k] for k in range(2)) for p in ps]
master = sum(p["bu"] * c for p, c in zip(ps, cm)) - F_b
flex = F(100) * (F(1000 * 100, 100) - F(100 * 0 + 100 * (2 * 50 + 1 * 200), 100)) - F_b
price = 0; volume = flex - master; mix = sum(p["au"] * c for p, c in zip(ps, cm)) - F_b - flex
eff = [s[k] * (sum(p["q"][k] * p["au"] for p in ps) - AQ[k]) for k in range(2)]
total = sum(p["au"] * p["ap"] for p in ps) - sum(a[k] * AQ[k] for k in range(2)) - F_a - master
print("witness total", total, "sum5 without ipv", price + volume + mix + sum(eff), "ipv", [(s[k]-a[k])*AQ[k] for k in range(2)])
