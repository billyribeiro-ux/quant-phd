"""Probe: compare each surviving projection mutant with the reference on random unit-diagonal inputs."""
from __future__ import annotations

import importlib.util
import math
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


def rand_matrix(rng: random.Random, k: int) -> list[list[float]]:
    m = [[0.0] * k for _ in range(k)]
    for i in range(k):
        m[i][i] = 1.0
        for j in range(i + 1, k):
            v = rng.uniform(-1.0, 1.0)
            m[i][j] = m[j][i] = v
    return m


def min_eig(m: list[list[float]]) -> float:
    return ref.min_eigenvalue(m)


rng = random.Random(12345)
worst: dict[str, tuple[float, str]] = {}
diag_dev: dict[str, float] = {}
psd_fail: dict[str, float] = {}
trials = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
for t in range(trials):
    k = rng.choice([2, 3, 4, 5, 6])
    a = rand_matrix(rng, k)
    r = ref.projection_repair(a)
    for name, mod in mods.items():
        y = mod.projection_repair(a)
        dev = max(abs(y[i][j] - r[i][j]) for i in range(k) for j in range(k))
        if dev > worst.get(name, (0.0, ""))[0]:
            worst[name] = (dev, repr(a))
        dd = max(abs(y[i][i] - 1.0) for i in range(k))
        diag_dev[name] = max(diag_dev.get(name, 0.0), dd)
        mp = min_eig(y)
        if mp < -1e-8:
            psd_fail[name] = min(psd_fail.get(name, 0.0), mp)
print("max entrywise |mutant - reference| over trials:")
for n, (d, _) in worst.items():
    print(n, d)
print("max |diag - 1| of mutant output:", diag_dev)
print("most negative min eig of mutant output (only if < -1e-8):", psd_fail)
