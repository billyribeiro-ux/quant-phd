"""Round-34 checks of L05 Lab 6's null count (line 873: 1.5 expected false rejections) and of the search-bound
sentence (line 722/873: a maximum over more rules is at least as large, so family-wide critical values are bounded).

The twin's data code (rules, exact integer scaling, d) is executed unchanged from tests/labs/S7/lab-S7-L05-6.py in a
scratch directory with data/fx_daily.csv. Then:
 (i) null count: d is demeaned (skill-free null); 2000 repetitions, each a stationary bootstrap resample of whole dates
     (mean block 10) of the demeaned rule returns; a rule rejects if its t = mean/se exceeds 1.645 (the per-rule
     one-sided 5% value the page uses). Reports the per-rule rejection rates, their range and the expected count
     (30 x rate). Tolerance: six standard errors of the expected count.
(ii) search bound: for B = 1000 draws, the 95% quantile of the maximum of centred bootstrap t* over the first m rules,
     m = 5, 10, 15, 20, 25, 30; nested maxima must give nondecreasing quantiles.
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r34/lab6_null_and_search.py <scratch-dir>
"""

from __future__ import annotations

import contextlib
import io
import math
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
TWIN = ROOT / "tests" / "labs" / "S7" / "lab-S7-L05-6.py"
FX = ROOT / "course" / "assets" / "data" / "market" / "fx_daily.csv"
scratch = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp())
work = scratch / "lab6_work"
(work / "data").mkdir(parents=True, exist_ok=True)
(work / "data" / "fx_daily.csv").write_bytes(FX.read_bytes())

import os  # noqa: E402

cwd = os.getcwd()
os.chdir(work)
ns: dict[str, object] = {"__name__": "lab6"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TWIN.read_text(encoding="utf-8"), str(TWIN), "exec"), ns)
os.chdir(cwd)
d = ns["d"]
assert isinstance(d, np.ndarray)
n_obs, n_rules = d.shape
print(f"twin data: {n_obs} days x {n_rules} rules")

def stationary(n: int, mean_block: float, gen: np.random.Generator, draws: int) -> np.ndarray:
    starts = gen.integers(0, n, size=(draws, n))
    new_block = gen.random((draws, n)) < 1.0 / mean_block
    new_block[:, 0] = True
    pos = np.arange(n)
    block_start = np.maximum.accumulate(np.where(new_block, pos, 0), axis=1)
    return np.asarray((starts[np.arange(draws)[:, None], block_start] + pos - block_start) % n, dtype=np.int64)

# (i) null count
gen = np.random.default_rng(341)
dd = d - d.mean(axis=0)
reps, chunk = 2000, 200
rej = np.zeros(n_rules)
for _ in range(reps // chunk):
    idx = stationary(n_obs, 10.0, gen, chunk)  # chunk x T
    for b in range(chunk):
        s = dd[idx[b]]
        t = s.mean(axis=0) / (s.std(axis=0, ddof=1) / math.sqrt(n_obs))
        rej += t > 1.645
rate = rej / reps
p = float(np.mean(rate))
se_rate = math.sqrt(p * (1 - p) / reps)
count = float(rate.sum())
se_count = math.sqrt(n_rules * p * (1 - p) / reps) * n_rules / math.sqrt(n_rules) * math.sqrt(n_rules) / math.sqrt(n_rules)
se_count = float(np.sqrt(np.sum(rate * (1 - rate) / reps)))
print(f"per-rule rejection rates: min {rate.min():.4f} max {rate.max():.4f} mean {p:.4f} (SE of one rate {se_rate:.4f})")
print(f"expected false rejections among {n_rules} rules: {count:.3f} (SE {se_count:.3f}); derivation 30 x 0.05 = 1.5")
print(f"page-quoted simulation value 1.395: |diff| {abs(count - 1.395):.3f} vs 6 SE {6 * se_count:.3f}")
ok_count = abs(count - 1.5) <= 6 * se_count
print(f"CHECK null count vs 1.5 within 6 SE: {'OK' if ok_count else 'FAILED'}")

# (ii) search bound: nested maxima
gen2 = np.random.default_rng(507)
Bn, alpha = 1000, 0.05
rank = math.ceil((1 - alpha) * Bn)
boots = []
for b0 in range(0, Bn, 100):
    idx = stationary(n_obs, 10.0, gen2, 100)
    for b in range(100):
        s = d[idx[b]]
        mu = d.mean(axis=0)
        boots.append((s.mean(axis=0) - mu) / (s.std(axis=0, ddof=1) / math.sqrt(n_obs)))
T = np.array(boots)
prev = -1.0
mono = True
for m in (5, 10, 15, 20, 25, 30):
    q = float(np.sort(T[:, :m].max(axis=1))[rank - 1])
    print(f"95% quantile of max over first {m} rules: {q:.4f}")
    mono = mono and q >= prev
    prev = q
print(f"CHECK nested quantiles nondecreasing: {'OK' if mono else 'FAILED'}")
