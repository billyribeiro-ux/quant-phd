"""Witness for AC1 L03 claim: a wrong depreciation amount still articulates (Check 5 alone fails).

Reads the lab twin read-only, writes two mutants to a scratch directory, runs each under python -I.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

TWIN = pathlib.Path("/tmp/verify8-AC1-a/tests/labs/AC1/lab-AC1-L03-1.py")
OUT = pathlib.Path("/tmp/ac1-v/a-r8")
PY = "/tmp/verify8-AC1-a/.venv/bin/python"
SRC_LINE = "            depreciation = 25_000_000 + (7_500_000 if year >= 2026 else 0)\n"

MUTANTS = {
    # one extra cent of depreciation in 2025 Q2, both sides of the entry move together
    "m_plus1cent_2025q2": SRC_LINE.replace(
        "depreciation = 25_000_000 + (7_500_000 if year >= 2026 else 0)",
        "depreciation = 25_000_000 + (7_500_000 if year >= 2026 else 0) + (1 if (year, quarter) == (2025, 2) else 0)",
    ),
    # a wrong quarterly charge in every quarter, consistently posted
    "m_wrong_rate": SRC_LINE.replace(
        "depreciation = 25_000_000 + (7_500_000 if year >= 2026 else 0)",
        "depreciation = 26_000_000 + (7_500_000 if year >= 2026 else 0)",
    ),
}


def main() -> int:
    source = TWIN.read_text(encoding="utf-8")
    if source.count(SRC_LINE) != 1:
        print("anchor line not found exactly once", file=sys.stderr)
        return 2
    for name, replacement in MUTANTS.items():
        path = OUT / f"{name}.py"
        path.write_text(source.replace(SRC_LINE, replacement), encoding="utf-8")
        result = subprocess.run([PY, "-I", "-W", "error", str(path)], capture_output=True, text=True, check=False)
        print(f"== {name} exit {result.returncode} stderr_bytes {len(result.stderr)}")
        for line in result.stdout.splitlines():
            if line.startswith("Check") or "True" in line or "False" in line:
                if "True" in line or "False" in line or line.startswith("Check"):
                    print("  " + line[:140])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
