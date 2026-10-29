"""Re-derive the seed-scan claims of L07 E1 and L08 E1 from the twins (round 20).

Loads each twin without running its main() call, then varies only the seed.
"""

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
results = {}
for lab in ("L07", "L08"):
    src = (ROOT / f"tests/labs/AC4/lab-AC4-{lab}-1.py").read_text(encoding="utf-8")
    assert src.rstrip().endswith("main()"), lab
    body = src.rstrip()[: -len("main()")]
    import types

    mod = types.ModuleType(f"twin_{lab}")
    sys.modules[mod.__name__] = mod
    exec(compile(body, f"lab-{lab}", "exec"), mod.__dict__)
    ns = mod.__dict__
    if lab == "L07":
        gen, t_min, t_max, displaced, nonempty, boundary = (
            ns["generate"], ns["t_min"], ns["t_max"], ns["displaced"], ns["nonempty"], ns["BOUNDARY"],
        )
        rows = []
        for seed in range(1, 41):
            cases = gen(seed, 200)
            fits = [c for c in cases if c.q <= c.capacity]
            empty = [c for c in fits if not nonempty(c)]
            rows.append((seed, len(fits), len(empty)))
        hits = [s for s, f, e in rows if f == 186 and e == 75]
        print("L07 seeds 1-40 (fits, empty):", [(s, f, e) for s, f, e in rows if f == 186 or e == 75])
        print("L07 seeds with 186 fits and 75 empty:", hits)
    else:
        generate = ns["generate"]
        DIV = ns["Division"]
        rows = []
        for seed in range(1, 41):
            divs = generate(seed, 8)
            count = 0
            for i, a in enumerate(divs):
                for b in divs[i + 1 :]:
                    x, y = (a, b) if a.name < b.name else (b, a)
                    by_ri = ns["residual_income"](x) - ns["residual_income"](y)
                    by_ratio = ns["return_ratio"](x) - ns["return_ratio"](y)
                    if (by_ri > 0) != (by_ratio > 0) and by_ri != 0 and by_ratio != 0:
                        count += 1
            rows.append((seed, count))
        print("L08 seeds 1-40 discordant counts:", rows)
        print("L08 seeds with 4 discordant:", [s for s, c in rows if c == 4])
        print("L08 seeds with other counts:", len([s for s, c in rows if c != 4]))
