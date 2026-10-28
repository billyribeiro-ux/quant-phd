"""Independent seed scan for the L07 and L08 twins: re-derives the counts the pages quote for seeds 1 to 40.

Reads each twin source, drops its trailing main() call, and execs the rest so the generators and
checks are the twin's own code. Run as: python -I seed_scan.py <checkout>.
"""

import sys
from pathlib import Path
from fractions import Fraction

root = Path(sys.argv[1])


def load(name: str) -> dict:
    src = (root / "tests/labs/AC4" / name).read_text(encoding="utf-8")
    src = src.rsplit("\nmain()", 1)[0]
    import types

    mod = types.ModuleType(name.replace("-", "_").replace(".py", ""))
    sys.modules[mod.__name__] = mod
    exec(compile(src, name, "exec"), mod.__dict__)
    return mod.__dict__


l07 = load("lab-AC4-L07-1.py")
rows07 = []
for seed in range(1, 41):
    cases = l07["generate"](seed, 200)
    fits = [c for c in cases if c.q <= c.capacity]
    empty = [c for c in fits if not l07["nonempty"](c)] if "nonempty" in l07 else [
        c for c in fits if l07["t_min"](c) > l07["t_max"](c)
    ]
    rows07.append((seed, len(fits), len(empty)))
hits07 = [s for s, f, e in rows07 if f == 186 and e == 75]
print("L07 seeds 1-40 with (186 fits, 75 empty):", hits07)
print("L07 seeds 1-40 with 75 empty (any fit count):", [s for s, f, e in rows07 if e == 75])
print("L07 seeds 1-40 with 186 fits (any empty count):", [s for s, f, e in rows07 if f == 186])
print("L07 seed 20261027 fit/empty:", [r for r in rows07 if r[0] == 20261027] or "outside 1-40 (checked separately)")

l08 = load("lab-AC4-L08-1.py")
counts = {}
for seed in range(1, 41):
    divs = l08["generate"](seed, 8)
    rr = l08["residual_income"]
    ro = l08["return_ratio"]
    n = 0
    for i, a in enumerate(divs):
        for b in divs[i + 1 :]:
            by_ri = rr(a) - rr(b)
            by_ratio = ro(a) - ro(b)
            if (by_ri > 0) != (by_ratio > 0) and by_ri != 0 and by_ratio != 0:
                n += 1
    counts[seed] = n
print("L08 seeds 1-40 discordant counts (of 28):", counts)
print("L08 seeds with count 4:", [s for s, n in counts.items() if n == 4])
print("L08 seeds with count != 4:", sum(1 for n in counts.values() if n != 4))
