"""Round-34 variant runs of the S7 L05-L06 lab twins (verifier scratch copies; repo twins are never edited).

Each variant is the repository twin with one stated parameter changed, written to a scratch file and run with
python -I -W error in a scratch directory that holds data/fx_daily.csv. Outputs are printed and saved.
Usage: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r34/variant_runs.py <scratch-dir>
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TWINS = ROOT / "tests" / "labs" / "S7"
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
PY = str(ROOT / ".venv" / "bin" / "python")
FX = ROOT / "course" / "assets" / "data" / "market" / "fx_daily.csv"


def run(name: str, source: str) -> str:
    with tempfile.TemporaryDirectory(dir=OUT) as work:
        w = Path(work)
        (w / "data").mkdir()
        (w / "data" / "fx_daily.csv").write_bytes(FX.read_bytes())
        script = w / f"{name}.py"
        script.write_text(source, encoding="utf-8")
        res = subprocess.run([PY, "-I", "-W", "error", str(script)], cwd=w, capture_output=True, text=True, check=False)
    text = f"== {name} rc={res.returncode} stderr_bytes={len(res.stderr)}\n{res.stdout}{res.stderr}"
    (OUT / f"{name}.out").write_text(text, encoding="utf-8")
    print(text)
    return text


def swap(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, old
    return src.replace(old, new)


L051 = (TWINS / "lab-S7-L05-1.py").read_text(encoding="utf-8")
for rho in ("0.0", "0.9"):
    run(f"L05-1-rho{rho}", swap(L051, "n_strat, rho, alpha, n_draws, n_reps = 20, 0.3,", f"n_strat, rho, alpha, n_draws, n_reps = 20, {rho},"))

L062 = (TWINS / "lab-S7-L06-2.py").read_text(encoding="utf-8")
run("L06-2-universes60", swap(L062, "universes = (slice(0, 30), slice(30, 60), slice(0, 60))", "universes = (slice(0, 60),)"))
run("L06-2-base", L062)

L061 = (TWINS / "lab-S7-L06-1.py").read_text(encoding="utf-8")
for share in ("0.2", "0.05", "0.5"):
    full = swap(L061, "effect = rng.random(m) < 0.2", f"effect = rng.random(m) < {share}")
    run(f"L06-1-full-share{share}", full)
    restricted = swap(full, "for m in (10, 100, 316, 1000, 10000):", "for m in (1000,):")
    run(f"L06-1-m1000-only-share{share}", restricted)
