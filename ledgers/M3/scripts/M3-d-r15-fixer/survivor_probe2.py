"""Probe 2: adversarial families (near-1 correlations, planted near-zero spectra, larger k)."""
from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/quant-b2")
REF = ROOT / "course/modules/M/M3/grader/reference.py"
MUTS = {
    "r6d_m04": ROOT / "ledgers/M3/mutants/r6d_m04_projection_stops_on_gap_only.py",
    "r9d_m02": ROOT / "ledgers/M3/mutants/r9d_m02_projection_returns_last_psd_iterate.py",
    "r11d_m02": next((ROOT / "ledgers/M3/mutants").glob("r11d_m02*.py")),
}


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(REF, "ref")
mods = {k: load(v, k) for k, v in MUTS.items()}
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
trials = int(sys.argv[1]) if len(sys.argv) > 1 else 500
best: dict[str, tuple[float, str]] = {}
diag: dict[str, tuple[float, str]] = {}
psdf: dict[str, tuple[float, str]] = {}


def family(k: int) -> list[list[float]]:
    kind = rng.choice(["near1", "lowrank", "mixed"])
    m = [[1.0 if i == j else 0.0 for j in range(k)] for i in range(k)]
    for i in range(k):
        for j in range(i + 1, k):
            if kind == "near1":
                v = rng.choice([-1, 1]) * rng.uniform(0.9, 0.9999)
            elif kind == "lowrank":
                v = 0.0
            else:
                v = rng.uniform(-0.999, 0.999)
            m[i][j] = m[j][i] = v
    if kind == "lowrank":
        # factor model with near-collinear loadings: a PSD-ish matrix with near-zero eigenvalues plus a perturbation
        f = [[rng.gauss(0, 1) for _ in range(2)] for _ in range(k)]
        rows = [[sum(f[i][c] * f[j][c] for c in range(2)) for j in range(k)] for i in range(k)]
        d = [max(rows[i][i], 1e-9) ** 0.5 for i in range(k)]
        m = [[rows[i][j] / (d[i] * d[j]) for j in range(k)] for i in range(k)]
        m[0][1] = m[1][0] = m[0][1] + rng.uniform(-0.6, 0.6)
    return m


for t in range(trials):
    k = rng.choice([3, 4, 5, 6, 7, 8])
    a = family(k)
    try:
        r = ref.projection_repair(a)
    except ValueError:
        continue
    for name, mod in mods.items():
        y = mod.projection_repair(a)
        dev = max(abs(y[i][j] - r[i][j]) for i in range(k) for j in range(k))
        dd = max(abs(y[i][i] - 1.0) for i in range(k))
        mp = ref.min_eigenvalue(y)
        if dev > best.get(name, (0.0, ""))[0]:
            best[name] = (dev, repr(a))
        if dd > diag.get(name, (0.0, ""))[0]:
            diag[name] = (dd, repr(a))
        if mp < psdf.get(name, (0.0, ""))[0]:
            psdf[name] = (mp, repr(a))
for n in MUTS:
    print(n, "maxdev", best.get(n, (None,))[0], "maxdiagdev", diag.get(n, (None,))[0], "minEig", psdf.get(n, (None,))[0])
for n, v in best.items():
    if v[0] > 1e-7:
        print("LARGE", n, v[0], v[1][:400])
