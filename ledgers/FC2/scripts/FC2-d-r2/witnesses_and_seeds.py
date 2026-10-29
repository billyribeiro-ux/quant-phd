"""FC2-d round 2: over-constraint witnesses and the seed sweep for the five alternatives and the witnesses.

Usage: .venv/bin/python -I ledgers/FC2/scripts/FC2-d-r2/witnesses_and_seeds.py <checkout> <scratch>
Builds w1 (capitalised rule names in explanations, from alt1) and w2 (memoised scan, from alt1) under <scratch>,
copies the grader suite and instance.py next to each, then runs the suite for seeds 0-49 and prints pass counts.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
grader = root / "course/modules/FC/FC2/grader"
scripts = root / "ledgers/FC2/scripts/FC2-d-r2"
src = (scripts / "alt1_fraction_scanner.py").read_text(encoding="utf-8")

w1 = src.replace('"explanation": f"put-call parity', '"explanation": f"Put-call parity')
w1 = w1.replace('"explanation": "convexity in strike', '"explanation": "Convexity in strike')
w1 = w1.replace('"Put-call parity', '"Parity').replace('f"Put-call parity', 'f"Parity')
assert w1.count("Convexity in strike") == 1, "w1 edit failed"
w2 = src.replace(
    "def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:\n",
    "_MEMO: dict[str, list[dict[str, Any]]] = {}\n\n\n"
    "def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:\n"
    "    key = repr(chain)\n    if key in _MEMO:\n        return _MEMO[key]\n    _MEMO[key] = _scan(chain)\n    return _MEMO[key]\n\n\n"
    "def _scan(chain: dict[str, Any]) -> list[dict[str, Any]]:\n",
    1,
)
assert w2 != src, "w2 edit failed"

variants = {
    "alt1": src,
    "alt2": (scripts / "alt2_integer_scanner.py").read_text(encoding="utf-8"),
    "alt3": (scripts / "alt3_float_scanner.py").read_text(encoding="utf-8"),
    "alt4": (scripts / "alt4_slope_scanner.py").read_text(encoding="utf-8"),
    "alt5": (scripts / "alt5_forward_scanner.py").read_text(encoding="utf-8"),
    "w1_capitalised_rule_names": w1,
    "w2_memoised_scan": w2,
}
python = sys.executable
for name, text in variants.items():
    work = scratch / name
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    shutil.copy(grader / "test_project.py", work)
    shutil.copy(grader / "instance.py", work)
    (work / "scanner.py").write_text(text, encoding="utf-8")
    passed = 0
    failing = []
    for seed in range(50):
        result = subprocess.run(
            [
                python,
                "-m",
                "pytest",
                "-q",
                "-p",
                "no:cacheprovider",
                "--assert=plain",
                "-W",
                "error",
                "test_project.py",
            ],
            cwd=work,
            capture_output=True,
            text=True,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            check=False,
        )
        if result.returncode == 0:
            passed += 1
        else:
            failing.append(seed)
    print(f"{name}: {passed}/50 seeds pass; first failing seeds {failing[:5]}")
