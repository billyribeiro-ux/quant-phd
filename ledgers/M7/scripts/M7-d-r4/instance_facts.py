"""Facts about make_instance over seeds 0-49: decimal digits of every payload float (from its repr), feasibility read
as exact decimals (the grader reads each number from its decimal text), asset counts, two sectors, determinism."""
import sys, json
from decimal import Decimal
sys.path.insert(0, sys.argv[1])
from instance import make_instance

max_digits = 0
fails = []
counts = {}


def walk(o):
    global max_digits
    if isinstance(o, float):
        e = Decimal(repr(o)).as_tuple().exponent
        max_digits = max(max_digits, -e if e < 0 else 0)
    elif isinstance(o, list):
        for v in o:
            walk(v)
    elif isinstance(o, dict):
        for v in o.values():
            walk(v)


for s in range(50):
    inst = make_instance(s)
    assert make_instance(s) == inst
    case = json.loads(inst["payload"])
    assert inst["label"].startswith("SIMULATED")
    walk(case)
    n = len(case["mu"])
    counts[n] = counts.get(n, 0) + 1
    assert len(case["sector_caps"]) == 2 and set(case["sector"]) == {0, 1}
    D = lambda x: Decimal(repr(x))
    w0 = [D(x) for x in case["w0"]]
    ok = (
        sum(w0) == 1
        and all(D(case["lower"][i]) <= w0[i] <= D(case["upper"][i]) for i in range(n))
        and all(
            sum((w0[i] for i in range(n) if case["sector"][i] == k), Decimal(0)) <= D(case["sector_caps"][k])
            for k in range(len(case["sector_caps"]))
        )
        and D(case["turnover_limit"]) >= 0
    )
    if not ok:
        fails.append(s)
print("max digits after the point (decimal text of payload floats), seeds 0-49:", max_digits)
print("exact-decimal feasibility failures:", fails)
print("asset counts over seeds 0-49:", dict(sorted(counts.items())))
