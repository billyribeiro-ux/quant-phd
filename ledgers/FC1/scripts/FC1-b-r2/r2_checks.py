"""FC1 slice b (L04-L05), verifier round 2. Re-derives the numbers and lab claims cited in the fragment.

Usage: python -I ledgers/FC1/scripts/FC1-b-r2/r2_checks.py <checkout>
Reads the twins and the lesson pages from <checkout>; writes nothing into the repository.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from fractions import Fraction

root = Path(sys.argv[1]).resolve()
py = sys.executable
tmp = Path(tempfile.mkdtemp(prefix="fc1b-r2-"))


def run(script: Path) -> str:
    out = subprocess.run([py, "-I", "-W", "error", str(script)], capture_output=True, text=True, check=True)
    return out.stdout


def lab_text(name: str) -> str:
    return (root / "tests/labs/FC1" / name).read_text(encoding="utf-8")


# 1. Ratios and sums quoted on L05 and L04
np_, gross = 14282414, 68398886
print("L05 ratio exact", float(Fraction(np_, gross)), "to 5dp 0.20881?", f"{np_ / gross:.5f}")
print("L05 ratio half-up 3dp floor(1000*NP/G+1/2)", (2 * 1000 * np_ + gross) // (2 * gross))
print("E1 P5 share of gross", f"{11060360 / gross:.6f}", "share of net", f"{11060360 / np_:.6f}")
print("E2 negatives", 7411991 + 6656379 + 214044, "positives", 3222054 + 11060360)
print("L04 E3 5600/173 =", Fraction(5600, 173), f"{5600 / 173:.4f}")
print("L04 Example 1.3 cost", 60 * 1000 + 90 * 1100, "avg", Fraction(159000, 150))

# 2. Settlement and clearing offsets: change one parameter at a time, diff against the page run
base = run(root / "tests/labs/FC1/lab-FC1-L05-1.py").splitlines()
for label, pattern, repl in [
    ("settlement lag 3", r"^SETTLEMENT_LAG = 2 ", "SETTLEMENT_LAG = 3 "),
    ("clearing offset 3", r"^CLEARING_OFFSET = 0 ", "CLEARING_OFFSET = 3 "),
]:
    src = re.sub(pattern, repl, lab_text("lab-FC1-L05-1.py"), count=1, flags=re.M)
    f = tmp / f"{label.replace(' ', '_')}.py"
    f.write_text(src, encoding="utf-8")
    alt = run(f).splitlines()
    changed = [i + 1 for i, (a, b) in enumerate(zip(base, alt)) if a != b]
    print(f"L05 {label}: changed output lines {changed}")
    for i in changed:
        print("   base:", base[i - 1][:90])
        print("   alt :", alt[i - 1][:90])

# 3. L04 trace: best bid after event 7, and the end-of-run bid
l04 = run(root / "tests/labs/FC1/lab-FC1-L04-1.py").splitlines()
print("L04 trace event 7:", [x for x in l04 if x.startswith("event 7:")])
print("L04 end line:", [x for x in l04 if x.startswith("best bid and ask at the end")])

# 4. Every output line of each twin appears verbatim in its lesson page
for lesson, twin in [("L04", "lab-FC1-L04-1.py"), ("L05", "lab-FC1-L05-1.py")]:
    page = html.unescape((root / f"course/modules/FC/FC1/{lesson}.html").read_text(encoding="utf-8"))
    lines = run(root / "tests/labs/FC1" / twin).splitlines()
    missing = [x for x in lines if x not in page]
    print(f"{lesson} twin output lines {len(lines)}, not verbatim in page: {len(missing)}")

# 5. R1 cascade on the L04 twin's own Book class
import importlib.util

stripped = tmp / "twin_l04_nomain.py"
stripped.write_text(lab_text("lab-FC1-L04-1.py").replace("\nmain()", "\n"), encoding="utf-8")
spec = importlib.util.spec_from_file_location("twin_l04_nomain", stripped)
assert spec is not None and spec.loader is not None
twin = importlib.util.module_from_spec(spec)
sys.modules["twin_l04_nomain"] = twin
spec.loader.exec_module(twin)
Book, Order = twin.Book, twin.Order
b = Book()  # type: ignore[operator]
b.match(Order(0, -1, "limit", 100, price=990))  # type: ignore[operator]
b.match(Order(1, 1, "limit", 100, price=985))  # type: ignore[operator]
b.match(Order(2, 1, "limit", 100, price=980))  # type: ignore[operator]
b.pending += [Order(3, -1, "stop", 100, stop=990), Order(4, -1, "stop", 100, stop=985)]  # type: ignore[operator]
b.activate()  # type: ignore[operator]
b.match(Order(5, 1, "market", 100))  # type: ignore[operator]
b.activate()  # type: ignore[operator]
print("R1 cascade fills", b.fills, "pending", len(b.pending))  # type: ignore[operator]
