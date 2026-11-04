"""Instance sample (seeds 0..19 and 1000..1019), starter-suite run, and internal link check for project.html.

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r5/instances_and_links_r5.py <repo_root>
"""

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction

root = sys.argv[1]
grader = os.path.join(root, "course", "modules", "FC", "FC2", "grader")
sys.path.insert(0, grader)
import instance as inst  # noqa: E402  (grader module, imported from the repo, read only)

PPM = 1_000_000
seeds = list(range(20)) + list(range(1000, 1020))
ok_all = True
answers = set()
for s in seeds:
    d = inst.make_instance(s)
    st, cs, ps, sp = d["strikes_cents"], d["call_cents"], d["put_cents"], d["spot_cents"]
    df = d["df_ppm"]
    valid = (
        len(st) == 6 and all(a < b for a, b in zip(st, st[1:])) and st[0] > 0
        and 1 <= df <= PPM and d["fee_cents_per_contract"] >= 0 and d["half_spread_cents"] >= 0
        and d["label"] == "SIMULATED" and len(cs) == len(ps) == 6
    )
    # the chain is parity-consistent except at the planted strike; calls are convex unless planted
    gaps = [Fraction(cs[k]) - Fraction(ps[k]) - (Fraction(sp) - Fraction(st[k] * df, PPM)) for k in range(6)]
    ok_all &= valid
    answers.add((d["planted_kind"], d["planted_index"], d["planted_amount_cents"], tuple(st), sp, df))
    print(s, "valid", valid, "planted", d["planted_kind"], d["planted_index"], d["planted_amount_cents"],
          "strikes", st[0], "..", st[-1], "df", df, "fee", d["fee_cents_per_contract"], "spread", d["half_spread_cents"])
print("all 40 valid:", ok_all, "| distinct (kind, index, amount, strikes, spot, df) tuples:", len(answers))

with tempfile.TemporaryDirectory() as tmp:
    shutil.copy(os.path.join(grader, "starter.py"), os.path.join(tmp, "scanner.py"))
    for name in ("instance.py", "test_project.py"):
        shutil.copy(os.path.join(grader, name), tmp)
    out = subprocess.run([os.path.join(root, ".venv", "bin", "python"), "-m", "pytest", "-q", "-p", "no:cacheprovider",
                          "--assert=plain", "-W", "error", "test_project.py"],
                         cwd=tmp, env=dict(os.environ, QF_SEED="0"), capture_output=True, text=True)
    print("starter.py suite rc", out.returncode, "(nonzero means the suite fails on the starter)")
    print(out.stdout.strip().splitlines()[-1])

page = open(os.path.join(root, "course", "modules", "FC", "FC2", "project.html"), encoding="utf-8").read()
ids = set(re.findall(r'\sid="([^"]+)"', page))
hrefs = re.findall(r'href="#([^"]+)"', page)
missing = sorted({h for h in hrefs if h not in ids})
print("internal #links:", len(hrefs), "targets missing:", missing)
files = sorted(set(re.findall(r'href="(grader/[^"]+)"', page)))
print("local grader links:", files, [os.path.exists(os.path.join(root, "course", "modules", "FC", "FC2", f)) for f in files])
