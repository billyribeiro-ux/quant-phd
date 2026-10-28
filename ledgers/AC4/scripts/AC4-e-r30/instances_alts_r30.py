"""Samples 20 seeds: each instance is valid, and the reference answers differ across seeds. Also duplicate scan of cards."""
import importlib.util, json, pathlib, sys, collections
ROOT = pathlib.Path(sys.argv[1]); G = ROOT / "course/modules/AC/AC4/grader"
sys.path.insert(0, str(G))
from instance import make_instance
spec = importlib.util.spec_from_file_location("ref", G / "reference.py"); ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
seeds = list(range(0, 50, 50 // 20))[:20]
answers = []
for sd in seeds:
    case = json.loads(make_instance(sd)["payload"])
    assert all(type(case[k]) is int for k in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used"))
    assert len(case["products"]) == 3 and len({p["name"] for p in case["products"]}) == 3
    for p in case["products"]:
        assert all(type(p[k]) is int for k in ("budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"))
        assert p["budget_price_cents"] > p["standard_inputs_per_unit"] * case["input_price_cents"]
    v = ref.variance_decomposition(case)
    answers.append((sd, tuple(v.values())))
print("seeds", seeds)
print("distinct answer tuples over 20 seeds:", len({a for _, a in answers}))
print("distinct sales_mix signs:", sorted({ (a[2] > 0) - (a[2] < 0) for _, a in answers}))
for sd, a in answers[:5]:
    print(sd, a)
cards = json.loads((ROOT / "course/modules/AC/AC4/cards.json").read_text(encoding="utf-8"))
print("card fronts duplicated:", [k for k, n in collections.Counter(c["front"] for c in cards).items() if n > 1])
print("card backs duplicated:", [k[:60] for k, n in collections.Counter(c["back"] for c in cards).items() if n > 1])
