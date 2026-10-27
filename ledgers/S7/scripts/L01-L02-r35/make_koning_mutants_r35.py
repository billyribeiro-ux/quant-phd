"""Round-35 mutants of the committed Koning spot check (tests/test_koning_spot.py), one change each.

Writes ledgers/S7/mutants/koning-r35/<name>.py (a complete copy of the test, with a leading comment that
names the error) and runs pytest on each copy and on the committed test. Prints the pass/fail counts.
Run: .venv/bin/python ledgers/S7/scripts/L01-L02-r35/make_koning_mutants_r35.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = (ROOT / "tests" / "test_koning_spot.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers" / "S7" / "mutants" / "koning-r35"
PY = str(ROOT / ".venv" / "bin" / "python")

MUTANTS: dict[str, tuple[str, str, str]] = {
    # name: (description, old, new)
    "cutoff-wrong-quantile": (
        "cutoff uses the two-sided 0.975 quantile instead of the one-sided 0.95 quantile (size ~0.025)",
        "cutoff = stats.norm.ppf(1 - LEVEL) * np.sqrt(N)",
        "cutoff = stats.norm.ppf(1 - 0.025) * np.sqrt(N)",
    ),
    "conditional-variance-off-by-one": (
        "phi_n uses the conditional variance N-j instead of N-(j+1), so the martingale is broken",
        "np.sqrt(N - (j + 1))",
        "np.sqrt(N - j)",
    ),
    "look-ahead-stop": (
        "stopping rule reads phi at its maximum over all looks (look-ahead), not the first crossing",
        "first = np.where(hit.any(axis=1), hit.argmax(axis=1), N - 1)",
        "first = phi.argmax(axis=1)",
    ),
    "claim-3-changed": (
        "phi_N is scaled by 0.999, so phi_N differs from the fixed-N test (claim 3 broken)",
        "phi[:, -1] = reject",
        "phi[:, -1] = 0.999 * reject",
    ),
    "cutoff-inflated-2pct": (
        "cutoff inflated by 2 percent, so the fixed-N size falls to about 0.0465 (level too low)",
        "cutoff = stats.norm.ppf(1 - LEVEL) * np.sqrt(N)",
        "cutoff = 1.02 * stats.norm.ppf(1 - LEVEL) * np.sqrt(N)",
    ),
}


def run(path: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [PY, "-m", "pytest", "-p", "no:cacheprovider", "-q", "--no-header", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    summary = [ln for ln in proc.stdout.splitlines() if " passed" in ln or " failed" in ln or " error" in ln]
    failed = [ln.split("::")[-1] for ln in proc.stdout.splitlines() if ln.startswith("FAILED ")]
    tail = (summary[-1] if summary else proc.stderr.strip()) + (f" | failing: {failed}" if failed else "")
    return proc.returncode, tail


OUT.mkdir(parents=True, exist_ok=True)
rc0, tail0 = run(ROOT / "tests" / "test_koning_spot.py")
print(f"committed test: rc={rc0}: {tail0}")
killed = 0
for name, (desc, old, new) in MUTANTS.items():
    assert SRC.count(old) == 1, f"{name}: target line must occur exactly once"
    body = SRC.replace(old, new)
    assert body != SRC
    path = OUT / f"{name}.py"
    path.write_text(f"# MUTANT {name}: {desc}\n" + body, encoding="utf-8")
    rc, tail = run(path)
    killed += rc != 0
    print(f"{name}: rc={rc}: {tail}")
print(f"killed {killed}/{len(MUTANTS)}")
sys.exit(0 if killed == len(MUTANTS) and rc0 == 0 else 1)
