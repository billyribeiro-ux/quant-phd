"""LX2 slice c, round 1: run the Lab 2 completion mutants and the alternative implementation against the page's expected block.

Run as: python3 -I -W error ledgers/LX2/scripts/LX2-c-r1/lab2_mutants.py
For every ledgers/LX2/mutants/*.py: a file named mut-* must FAIL the instant check (output differs from the page's
expected block of lab-LX2-project-2, or exit != 0); a file named alt-* must PASS it.
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
page = (ROOT / "course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
m = re.search(r'<section class="lab completion" id="lab-LX2-project-2".*?<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
expected = html.unescape(m.group(1)).rstrip("\n")
bad = 0
for path in sorted((ROOT / "ledgers/LX2/mutants").glob("*.py")):
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True)
    same = run.returncode == 0 and run.stdout.rstrip("\n") == expected
    killed = not same
    want_kill = path.name.startswith("mut-")
    verdict = "OK" if killed == want_kill else "WRONG"
    if verdict != "OK":
        bad += 1
    with open(path, encoding="utf-8") as fh:
        first = fh.readline().strip()
    print(f"{path.name}: killed={killed} expected_kill={want_kill} {verdict} | {first}")
print("RESULT", "PASS" if bad == 0 else "FAIL", "mismatches=", bad)
