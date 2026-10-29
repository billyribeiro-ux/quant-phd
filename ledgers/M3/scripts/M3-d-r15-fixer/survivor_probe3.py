"""Probe 3: r6d_m04 and r11d_m02 versus reference across tol and max_iter; named-property check."""
from __future__ import annotations

import importlib.util
import random
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/quant-b2")


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(ROOT / "course/modules/M/M3/grader/reference.py", "ref")
m6 = load(ROOT / "ledgers/M3/mutants/r6d_m04_projection_stops_on_gap_only.py", "m6")
m11 = load(next((ROOT / "ledgers/M3/mutants").glob("r11d_m02*.py")), "m11")
rng = random.Random(99)
for tol in (1e-10, 1e-6, 1e-3):
    for mi in (1, 2, 3, 5, 500):
        worst = {"m6": 0.0, "m11": 0.0}
        psd_bad = {"ref": 0.0, "m6": 0.0, "m11": 0.0}
        for _ in range(300):
            k = rng.choice([3, 4, 5])
            a = [[1.0 if i == j else 0.0 for j in range(k)] for i in range(k)]
            for i in range(k):
                for j in range(i + 1, k):
                    a[i][j] = a[j][i] = rng.uniform(-0.99, 0.99)
            r = ref.projection_repair(a, tol=tol, max_iter=mi)
            for nm, mod in (("m6", m6), ("m11", m11)):
                y = mod.projection_repair(a, tol=tol, max_iter=mi)
                worst[nm] = max(worst[nm], max(abs(y[i][j] - r[i][j]) for i in range(k) for j in range(k)))
                psd_bad[nm] = max(psd_bad[nm], -ref.min_eigenvalue(y))
            psd_bad["ref"] = max(psd_bad["ref"], -ref.min_eigenvalue(r))
        print(f"tol={tol:g} max_iter={mi}: maxdev m6={worst['m6']:.3g} m11={worst['m11']:.3g} | worst -minEig ref={psd_bad['ref']:.3g} m6={psd_bad['m6']:.3g} m11={psd_bad['m11']:.3g}")
