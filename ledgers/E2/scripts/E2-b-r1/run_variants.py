"""E2 slice b verifier script: run the page exercises' variant twins (L04 e1/e2, L05 e1, L06 e1) in scratch copies.

Usage: <checkout>/.venv/bin/python -I <checkout>/ledgers/E2/scripts/E2-b-r1/run_variants.py <checkout> <scratch_dir>
The twins in the checkout are read only; each variant is a changed copy written under <scratch_dir>.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
twins = root / "tests/labs/E2"
py = root / ".venv/bin/python"
variants = {
    "L04-e1": ("lab-E2-L04-1.py", [("COST_HIGH = 500_000", "COST_HIGH = 400_000")]),
    "L04-e2": ("lab-E2-L04-1.py", [("Y_HIGH = 6_000_000", "Y_HIGH = 5_000_000")]),
    "L05-e1": ("lab-E2-L05-1.py", [("P_LOW = Fraction(3, 4)", "P_LOW = Fraction(2, 3)"),
                                   ("P_HIGH = Fraction(1, 4)", "P_HIGH = Fraction(1, 3)")]),
    "L06-e1": ("lab-E2-L06-1.py", [("COST_HIGH = 100_000 ", "COST_HIGH = 150_000 ")]),
}
for name, (twin, subs) in variants.items():
    text = (twins / twin).read_text(encoding="utf-8")
    for old, new in subs:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    out = scratch / f"{name}.py"
    out.write_text(text, encoding="utf-8")
    proc = subprocess.run([str(py), "-I", "-W", "error", str(out)], capture_output=True, text=True, timeout=20)
    print(f"== {name} rc={proc.returncode} stderr_bytes={len(proc.stderr)}")
    print(proc.stdout.rstrip())
