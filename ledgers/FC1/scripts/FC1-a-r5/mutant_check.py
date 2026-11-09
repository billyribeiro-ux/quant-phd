"""Run each lab-claim mutant under python -I -W error and compare stdout with the page's expected block."""
import html
import re
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyS5-FC1-a"
PAGE = {"L01": "course/modules/FC/FC1/L01.html", "L02": "course/modules/FC/FC1/L02.html", "L03": "course/modules/FC/FC1/L03.html"}
MUT = {
    "L01": "ledgers/FC1/mutants/fc1a_r5_lab_L01_half_limit_comparison_flipped.py",
    "L02": "ledgers/FC1/mutants/fc1a_r5_lab_L02_well_formed_accepts_two_values.py",
    "L03": "ledgers/FC1/mutants/fc1a_r5_lab_L03_tie_pays_full_profit.py",
}
for lesson in ("L01", "L02", "L03"):
    src = open(f"{ROOT}/{PAGE[lesson]}", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(m.group(1)).rstrip("\n").splitlines()
    for label, path in (("twin", f"{ROOT}/tests/labs/FC1/lab-FC1-{lesson}-1.py"), ("mutant", f"{ROOT}/{MUT[lesson]}")):
        r = subprocess.run([f"{ROOT}/.venv/bin/python", "-I", "-W", "error", path], capture_output=True, text=True)
        got = r.stdout.rstrip("\n").splitlines()
        diffs = [(i, e, g) for i, (e, g) in enumerate(zip(expected, got)) if e != g]
        if len(expected) != len(got):
            diffs.append(("len", len(expected), len(got)))
        print(f"{lesson} {label} exit={r.returncode} stderr_bytes={len(r.stderr)} expected_lines={len(expected)} got_lines={len(got)} mismatches={len(diffs)}")
        for d in diffs[:3]:
            print("   ", d)
