# Independent check: (a) every number the reference returns is an int; (b) stretch identities with two inputs and with spending variances.
import sys, random, importlib.util, itertools
from fractions import Fraction
spec = importlib.util.spec_from_file_location("ref", sys.argv[1]); ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
def leaves(x):
    if isinstance(x, dict):
        for v in x.values(): yield from leaves(v)
    elif isinstance(x, (list, tuple)):
        for v in x: yield from leaves(v)
    else: yield x
case = {"input_price_cents": 500, "fixed_overhead_cents": 1000000, "actual_inputs_used": 5300,
        "products": [
            {"name": "A", "budget_units": 1000, "budget_price_cents": 2500, "standard_inputs_per_unit": 2, "actual_units": 1200, "actual_price_cents": 2400},
            {"name": "B", "budget_units": 800, "budget_price_cents": 3400, "standard_inputs_per_unit": 3, "actual_units": 900, "actual_price_cents": 3450}]}
outs = [ref.master_budget(case), ref.flexible_budget(case, 2100), ref.variance_decomposition(case)]
print("all leaves int:", all(type(v) is int for o in outs for v in leaves(o)))
# (b) random two-input and spending-variance identities, exact fractions
random.seed(1)
bad_two = bad_spend = 0
for _ in range(2000):
    n = random.randint(1, 4)
    bu = [random.randint(1, 500) for _ in range(n)]; au = [random.randint(0, 600) for _ in range(n)]
    bp = [random.randint(100, 5000) for _ in range(n)]; ap = [random.randint(100, 5000) for _ in range(n)]
    q1 = [random.randint(0, 4) for _ in range(n)]; q2 = [random.randint(0, 4) for _ in range(n)]
    s1 = random.randint(1, 900); s2 = random.randint(1, 900); a1 = random.randint(1, 900); a2 = random.randint(1, 900)
    AQ1 = random.randint(0, 3000); AQ2 = random.randint(0, 3000); F = random.randint(0, 10**6); FA = random.randint(0, 10**6)
    BU = sum(bu); AT = sum(au)
    # two inputs: exact profits
    bud_profit = sum(bu[i] * (bp[i] - q1[i]*s1 - q2[i]*s2) for i in range(n)) - F
    act_profit = sum(au[i] * ap[i] for i in range(n)) - a1*AQ1 - a2*AQ2 - FA
    mcm = lambda i: bp[i] - q1[i]*s1 - q2[i]*s2
    flex_profit = Fraction(AT, BU) * sum(bu[i]*(bp[i]) for i in range(n)) - Fraction(AT, BU)*sum(bu[i]*(q1[i]*s1+q2[i]*s2) for i in range(n)) - F
    price = sum((ap[i]-bp[i])*au[i] for i in range(n))
    volume = flex_profit - bud_profit
    mix = sum(au[i]*mcm(i) for i in range(n)) - F - flex_profit
    eff1 = s1 * (sum(q1[i]*au[i] for i in range(n)) - AQ1)
    eff2 = s2 * (sum(q2[i]*au[i] for i in range(n)) - AQ2)
    total = act_profit - bud_profit
    if price + volume + mix + eff1 + eff2 != total: bad_two += 1
    # spending: input price variance (s-a)AQ per input, fixed overhead F-FA; the six figures
    ipv = (s1 - a1) * AQ1 + (s2 - a2) * AQ2
    fov = F - FA
    # with the fixed-overhead variance and the input price variance, the efficiency is at standard price
    if price + volume + mix + eff1 + eff2 + ipv + fov != total + (0): 
        # identity with spending variances should be: total = six figures (ipv, fov with favourable sign)
        bad_spend += 1
print("two-input identity failures:", bad_two, "of 2000")
print("six-figure identity failures (sign convention: favourable positive):", bad_spend, "of 2000")
