"""Round-6 recomputation of the hub's numbers: placement answers, hours split and the mastery bar.

Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-a-r6/recompute_hub_r6.py  (from the checkout root)
"""

import math
import re
from fractions import Fraction as F
from pathlib import Path

ROOT = Path.cwd()
hub = (ROOT / "course/modules/PC/PC3/index.html").read_text(encoding="utf-8")
fails = 0
checks = 0


def check(label: str, got: object, want: object) -> None:
    global fails, checks
    checks += 1
    ok = got == want
    fails += 0 if ok else 1
    print(f"{'PASS' if ok else 'FAIL'} {label}: got {got} want {want}")


answers = re.findall(r'data-answer="([^"]+)" data-tolerance="([^"]+)"', hub)
want = {
    "3.5": F(7, 2),  # 21/6
    "0.25": F(1, 4),
    "2": F(2),  # ln(e^2)
    "3": F(3),  # d/dx x^3 at 1
    "90.909091": F(100) / F(11, 10),  # 100/1.1 to six places
    "-10005": F(-10005),
    "10040": F(10040),
}
for ans, tol in answers:
    if ans in want:
        exact = want[ans]
        check(f"placement answer {ans} within tolerance {tol}", abs(float(exact) - float(ans)) <= float(tol) + 1e-15, True)
check("ln(e^2) = 2", math.log(math.exp(2)), 2.0)
check("ten-item bar: 80 percent of 10 = 8", F(8, 10) == F(80, 100) and 8 * 10 == 80 * 1, True)
check("seven of ten is 70 percent", F(7, 10), F(70, 100))
check("hours: 6 x 6 = 36", 6 * 6, 36)
check("hours: 2 + 6 + 4 + 2 = 14", 2 + 6 + 4 + 2, 14)
check("hours: 36 + 14 = 50", 36 + 14, 50)
check("project share 14/50 = 28 percent", round(100 * 14 / 50), 28)
check("lessons share 36/50 = 72 percent", round(100 * 36 / 50), 72)
check("hub data-hours-lessons=36", 'data-hours-lessons="36"' in hub, True)
check("hub data-hours-project=14", 'data-hours-project="14"' in hub, True)
check("hub hours-split widths 72% and 28%", ('style="width:72%"' in hub) and ('style="width:28%"' in hub), True)
print(f"SUMMARY checks={checks} fails={fails}")
