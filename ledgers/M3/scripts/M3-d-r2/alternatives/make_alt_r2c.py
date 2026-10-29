"""Writes alt_r2c_reference_other_cutoffs.py: the reference with different numerical cutoffs (Jacobi off-diagonal
cutoff 1e-12 instead of 1e-15 relative, 40 sweeps instead of 100, and an absolute Dykstra stop of tol on both norms).
Usage: make_alt_r2c.py <checkout-root>
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
src = (root / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
edits = [
    ("off <= 1e-15 * max(scale, 1e-300)", "off <= 1e-12"),
    ("for _ in range(100):", "for _ in range(40):"),
    ('"""Reference solution', '"""Alternative C (verifier round 2): reference with other numerical cutoffs.\n\nReference solution'),
]
out = src
for old, new in edits:
    assert out.count(old) == 1, old
    out = out.replace(old, new)
dest = Path(__file__).with_name("alt_r2c_reference_other_cutoffs.py")
dest.write_text(out, encoding="utf-8")
print("wrote", dest)
