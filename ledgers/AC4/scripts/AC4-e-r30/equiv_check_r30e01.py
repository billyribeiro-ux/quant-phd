"""Equivalence check for r30e_01 (total as sum of the four variances): random valid cases, exact identity."""
import importlib.util, random, sys, pathlib
from fractions import Fraction
ROOT = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("ref", ROOT / "course/modules/AC/AC4/grader/reference.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
rng = random.Random(30)
checked = 0
for _ in range(20000):
    n = rng.randint(1, 4)
    s = rng.randint(0, 400)
    prods = []
    for i in range(n):
        prods.append({"name": f"P{i}", "budget_units": rng.randint(0, 900), "budget_price_cents": rng.randint(0, 9000),
                      "standard_inputs_per_unit": rng.randint(0, 6), "actual_units": rng.randint(0, 900),
                      "actual_price_cents": rng.randint(0, 9000)})
    if sum(p["budget_units"] for p in prods) == 0:
        prods[0]["budget_units"] = 1
    case = {"input_price_cents": s, "fixed_overhead_cents": rng.randint(0, 10**6), "actual_inputs_used": rng.randint(0, 5000), "products": prods}
    v = ref.variance_decomposition(case)
    assert v["sales_price"] + v["sales_volume"] + v["sales_mix"] + v["efficiency"] == v["total"]
    # the mutant's total is the sum of the reference's four variances: identical by the assertion above
    checked += 1
print("identity held exactly on", checked, "random valid cases")
