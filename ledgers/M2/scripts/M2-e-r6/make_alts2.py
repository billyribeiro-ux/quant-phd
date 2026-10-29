"""Two more alternative correct implementations: (4) sensitivities by a backward Horner-style recursion with a
dual-number-free discount recursion and bond price by math.fsum; (5) the Hessian by the four-point off-diagonal formula
written in a different order, with the central estimate by Richardson and the forward estimate unchanged."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
ref = (ROOT / "course/modules/M/M2/grader/reference.py").read_text(encoding="utf-8")
OUT.mkdir(parents=True, exist_ok=True)


def edit(src, pairs):
    for old, new in pairs:
        assert src.count(old) == 1, old[:70]
        src = src.replace(old, new)
    return src


alt4 = edit(ref, [
    ("    flows, rate = _cash_flows(instance)\n    v = 1 / (1 + rate)\n    price = sum(cash * v**t for t, cash in flows)\n    return round(price)",
     "    import math\n    flows, rate = _cash_flows(instance)\n    v = 1 / (1 + rate)\n    price = math.fsum(cash * v**t for t, cash in flows)\n    return round(price)"),
    ("    flows, rate = _cash_flows(instance)\n    v = 1 / (1 + rate)\n    price = sum(cash * v**t for t, cash in flows)\n    first = -sum(t * cash * v ** (t + 1) for t, cash in flows)\n    second = sum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)",
     "    flows, rate = _cash_flows(instance)\n    v = 1 / (1 + rate)\n    # Horner-style backward recursion over the years: acc = sum of cash_s v^(s-t) for s >= t, from the last year back.\n    acc_p = acc_d = acc_s = 0.0\n    for t, cash in reversed(flows):\n        acc_p = cash + v * acc_p\n        acc_d = t * cash + v * acc_d\n        acc_s = t * (t + 1) * cash + v * acc_s\n    price = v * acc_p\n    first = -v * v * acc_d\n    second = v ** 3 * acc_s"),
])
(OUT / "alt4_horner_recursion_and_fsum.py").write_text(alt4, encoding="utf-8")

alt5 = edit(ref, [
    ("        for j in range(i + 1, n):\n            mixed = (\n                f(_moved(base, {i: step, j: step}))\n                - f(_moved(base, {i: step, j: -step}))\n                - f(_moved(base, {i: -step, j: step}))\n                + f(_moved(base, {i: -step, j: -step}))\n            )\n            hessian[i][j] = mixed / (4 * step * step)\n            hessian[j][i] = hessian[i][j]",
     "        for j in range(i + 1, n):\n            mixed = (\n                f(_moved(base, {j: -step, i: -step}))\n                - f(_moved(base, {j: step, i: -step}))\n                - f(_moved(base, {j: -step, i: step}))\n                + f(_moved(base, {j: step, i: step}))\n            )\n            hessian[i][j] = mixed / (4 * step * step)\n            hessian[j][i] = hessian[i][j]"),
    ("    if scheme == \"forward\":\n        return (f(x + step) - f(x)) / step\n    if scheme == \"central\":\n        return (f(x + step) - f(x - step)) / (2 * step)",
     "    if scheme == \"forward\":\n        return (f(x + step) - f(x)) / step\n    if scheme == \"central\":\n        half = step / 2\n        return (4 * ((f(x + half) - f(x - half)) / (2 * half)) - (f(x + step) - f(x - step)) / (2 * step)) / 3"),
])
(OUT / "alt5_reordered_mixed_and_richardson.py").write_text(alt5, encoding="utf-8")
print("wrote", sorted(p.name for p in OUT.iterdir()))
