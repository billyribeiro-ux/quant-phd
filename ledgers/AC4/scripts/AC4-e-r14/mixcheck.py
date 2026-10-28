import sys, random, pathlib
from fractions import Fraction
sys.path.insert(0, sys.argv[1] + "/course/modules/AC/AC4/grader")
import reference as sol
random.seed(14)
worst = Fraction(0); n = 0
for _ in range(20000):
    k = random.randint(1, 4)
    prods = []
    for i in range(k):
        prods.append({"name": f"P{i}", "budget_units": random.randint(0, 40), "budget_price_cents": random.randint(0, 999),
                      "standard_inputs_per_unit": random.randint(0, 9), "actual_units": random.randint(0, 40),
                      "actual_price_cents": random.randint(0, 999)})
    if sum(p["budget_units"] for p in prods) == 0:
        prods[0]["budget_units"] = 1
    case = {"input_price_cents": random.randint(0, 500), "fixed_overhead_cents": random.randint(0, 5000),
            "actual_inputs_used": random.randint(0, 500), "products": prods}
    got = sol.variance_decomposition(case)
    BU = sum(p["budget_units"] for p in prods); AT = sum(p["actual_units"] for p in prods)
    brev = sum(p["budget_units"] * p["budget_price_cents"] for p in prods)
    bvar = sum(p["budget_units"] * p["standard_inputs_per_unit"] * case["input_price_cents"] for p in prods)
    exact_flex = Fraction(AT * brev, BU) - Fraction(AT * bvar, BU) - case["fixed_overhead_cents"]
    mixc = sum(p["actual_units"] * (p["budget_price_cents"] - p["standard_inputs_per_unit"] * case["input_price_cents"]) for p in prods) - case["fixed_overhead_cents"]
    exact_mix = mixc - exact_flex
    d = abs(Fraction(got["sales_mix"]) - exact_mix)
    worst = max(worst, d); n += 1
print("cases", n, "max |mix - exact mix| =", float(worst), "strictly < 1:", worst < 1)
