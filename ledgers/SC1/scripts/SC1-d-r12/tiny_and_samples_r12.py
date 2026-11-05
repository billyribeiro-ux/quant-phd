"""(1) Numeric gap of the two surviving edge mutants against the page's 1e-10 statement; (2) 20-seed sample of instances and answers."""
import math
import random
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "course/modules/SC/SC1/grader"))
from instance import make_instance  # noqa: E402

print("(1) edge gaps against erfc(a/sqrt(2t)):")
for a, t in ((1e-7, 2.0), (1e-6, 0.5), (1e-9, 2.0)):
    exact = math.erfc(a / math.sqrt(2 * t))
    print(f"  a={a:g} t={t:g}: erfc={exact!r}; tiny-level mutant returns 1.0, gap {abs(1.0 - exact):.3e}")
for a, t in ((1e-3, 1e-7), (0.5, 1e-7), (2.0, 1e-7)):
    exact = math.erfc(a / math.sqrt(2 * t))
    print(f"  a={a:g} t={t:g}: erfc={exact:.6g}; tiny-time mutant returns 0.0, gap {abs(exact):.3e}")

print("(2) 20 seeds (0,3,...,57 spread): instances and answers")
rows = []
for seed in range(0, 60, 3):
    inst = make_instance(seed)
    rng = random.Random(inst["seed"])
    tail = math.erfc(inst["a"] / math.sqrt(2 * inst["H"]))
    rows.append((seed, inst["H"], inst["a"], inst["n_steps"], inst["n_paths"], round(tail, 6)))
for r in rows:
    print("  seed %2d H=%.3f a=%.3f n_steps=%3d n_paths=%3d tail=%.6f" % r)
print("  distinct tails:", len({r[5] for r in rows}), "of", len(rows), "; distinct levels:", len({r[2] for r in rows}))
