"""Round-18 LX1-c: distinguishing synthetic inputs for Lab 3 (verifier-written).

Runs the Lab 3 twin and each r18 Lab 3 mutant (python -I -W error) on seeded synthetic snapshots that have the
same header and months as fx_monthly.csv, and reports, per input, whether the printed output differs from the twin.
Also independently recomputes the difference and ratio from unrounded values with statistics.stdev.
Usage: python -I lab3_synth_r18.py <checkout_root>
"""
import csv
import io
import math
import pathlib
import random
import shutil
import statistics
import subprocess
import sys
import tempfile
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(sys.argv[1]).resolve()
TWIN = ROOT / "tests/labs/LX1/lab-LX1-project-3.py"
MUTS = sorted((ROOT / "ledgers/LX1/mutants").glob("lx1c_r18n0*.py"))
REAL = ROOT / "course/assets/data/market/fx_monthly.csv"


def months():
    out = []
    for y in range(1971, 2027):
        for m in range(1, 13):
            if (y, m) > (2026, 9):
                break
            out.append(f"{y}-{m:02d}")
    return out


def make_csv(path, seed, sigma_early, sigma_late, drift_late, tiny_every):
    rnd = random.Random(seed)
    ms = months()
    rate = Decimal("1.5")
    lines = ["month,GBP"]
    for i, m in enumerate(ms):
        if i > 0:
            sig = sigma_early if m < "2000-01" else sigma_late
            mu = 0.0 if m < "2000-01" else drift_late
            step = mu + rnd.gauss(0, sig)
            if tiny_every and i % tiny_every == 0:
                step = 0.00001
            rate = (rate * Decimal(repr(math.exp(step)))).quantize(Decimal("0.00000001"))
        lines.append(f"{m},{rate:.8f}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_one(script, csv_path):
    with tempfile.TemporaryDirectory(prefix="lx1c_r18_synth_") as tmp:
        (pathlib.Path(tmp) / "data").mkdir()
        shutil.copy(csv_path, pathlib.Path(tmp) / "data" / "fx_monthly.csv")
        p = subprocess.run([sys.executable, "-I", "-W", "error", str(script)], cwd=tmp,
                           capture_output=True, text=True, timeout=120)
    return p.returncode, p.stdout, p.stderr


def independent(csv_path):
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    ch = [(r["month"], math.log(float(Decimal(b["GBP"]) / Decimal(a["GBP"])))) for a, b in zip(rows, rows[1:]) for r in [b]]
    w1 = [v for _, v in ch]
    w2 = [v for m, v in ch if m >= "2000-01"]
    s1, s2 = statistics.stdev(w1), statistics.stdev(w2)
    ratio = Decimal(s2 / s1).quantize(Decimal("0.01"), ROUND_HALF_UP)
    diff = Decimal(100 * (s1 - s2)).quantize(Decimal("0.01"), ROUND_HALF_UP)
    diff_printed = Decimal(round(100 * s1, 2)) - Decimal(round(100 * s2, 2))
    return str(ratio), str(diff), str(diff_printed)


SCEN = [
    ("real", REAL),
]
cases = [
    ("drift2000_sig", dict(seed=1, sigma_early=0.02, sigma_late=0.02, drift_late=0.004, tiny_every=0)),
    ("tiny_moves", dict(seed=2, sigma_early=0.02, sigma_late=0.02, drift_late=0.0, tiny_every=50)),
]
for seed in range(3, 40):
    cases.append((f"rounding_seed{seed}", dict(seed=seed, sigma_early=0.0137, sigma_late=0.0161, drift_late=0.0, tiny_every=0)))

work = pathlib.Path(tempfile.mkdtemp(prefix="lx1c_r18_csv_"))
results = []
for name, kw in cases:
    p = work / f"{name}.csv"
    make_csv(p, **kw)
    SCEN.append((name, p))

for name, csv_path in SCEN:
    rc, out, err = run_one(TWIN, csv_path)
    if rc != 0 or err.strip():
        print(f"{name}: TWIN rc={rc} err={err.strip()[-200:]}")
        continue
    killed = []
    for m in MUTS:
        mrc, mout, merr = run_one(m, csv_path)
        if mrc != 0 or merr.strip() or mout != out:
            killed.append(m.name[:12])
    ratio, diff, diff_printed = independent(csv_path)
    twin_diff = [ln for ln in out.splitlines() if "difference of window" in ln][0].split(": ")[-1]
    twin_ratio = [ln for ln in out.splitlines() if "ratio of window two" in ln][0].split(": ")[-1]
    if name == "real" or name.startswith("drift") or name.startswith("tiny") or name.startswith("rounding_seed"):
        print(f"{name}: twin ratio={twin_ratio} indep ratio={ratio} | twin diff={twin_diff} indep diff={diff} printed-diff={diff_printed} | mutants distinguished={killed}")
shutil.rmtree(work, ignore_errors=True)
