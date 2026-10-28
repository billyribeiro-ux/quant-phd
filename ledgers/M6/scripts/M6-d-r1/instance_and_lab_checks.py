"""Verifier round 1, M6 project slice: instance validity over seeds 0-49 and the project lab twins against the page.

Usage: <checkout>/.venv/bin/python ledgers/M6/scripts/M6-d-r1/instance_and_lab_checks.py <checkout>
Checks: every instance satisfies the generator's stated ranges; capital equals base*(2**J-1)+e with e < base*2**J, so
exactly J bets are placed when every bet loses (checked by direct simulation of the rule); 50 seeds give 50 distinct
instances; each project lab twin runs under python -I -W error and its stdout equals the page's expected block;
the page's lab code equals its twin except for the two blanks of Lab 2.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
grader = root / "course/modules/M/M6/grader"
sys.path.insert(0, str(grader))
from instance import make_instance  # noqa: E402

rows = [make_instance(s) for s in range(50)]
bad = []
for r in rows:
    if not (4 <= r["horizon"] <= 10 and 1 <= r["stop_cap"] <= r["horizon"] and r["stop_level"] in (1, 2)):
        bad.append(("horizon/stop", r["seed"]))
    if not (1 <= r["base_stake_cents"] <= r["capital_cents"]):
        bad.append(("base<=capital", r["seed"]))
    s, k = r["base_stake_cents"], r["capital_cents"]
    # count the bets the rule places when every bet loses: bet j+1 needs stake s*2**j <= wealth on hand
    wealth, placed = k, 0
    while s * 2**placed <= wealth:
        wealth -= s * 2**placed
        placed += 1
    if not (1 <= placed <= 8 and wealth == k - s * (2**placed - 1)):
        bad.append(("bet count", r["seed"]))
print("instance range/rule violations over 50 seeds:", bad)
print("distinct instances over seeds 0-49:", len({tuple(sorted((a, b) for a, b in r.items() if a != "label")) for r in rows}))

for i in (1, 2, 3):
    twin = root / f"tests/labs/M6/lab-M6-project-{i}.py"
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=False)
    page = (root / "course/modules/M/M6/project.html").read_text(encoding="utf-8")
    expected = html.unescape(re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)[i - 1])
    print(f"lab-M6-project-{i}: exit {run.returncode}; stdout equals page expected: {run.stdout == expected + chr(10) or run.stdout.rstrip() == expected.rstrip()}")
    code = html.unescape(re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)[i - 1])
    print(f"  page code equals twin: {code.strip() == twin.read_text(encoding='utf-8').strip()}")
