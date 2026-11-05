"""Independent recomputation of the LX2 lab numbers that the cards and lesson sentences state (LX2-d round 9).

Usage: python3 -I ledgers/LX2/scripts/LX2-d-r9/lab_checks.py <checkout-root> <scratch-dir>
1. Runs each LX2 twin under python -I -W error (stdout captured; a non-zero exit or any stderr is printed).
2. Parses Part A of the L04 twin, re-derives error = forecast - realised and hit = |error| <= 2, and recomputes
   hits, hit rate, bias (sum/H), mean absolute error, and the 4-place display rule of Definition 4.1.
3. Enumerates Proposition 4.4: pairs (V, U) with V in -4..4 and U in -6..6, counting -3 <= V - U <= 1.
4. Experiment E3 of L02: copies the twin, sets P7's source_told_of_trade to False, and prints the summary lines.
5. Prints the L03 flagged-trader line and the L01 state-table rows that permit a sale.
"""

import json
import math
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
twins = root / "tests/labs/LX2"
outputs: dict[str, str] = {}
for lab in ("L01", "L02", "L03", "L04"):
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twins / f"lab-LX2-{lab}-1.py")],
        capture_output=True,
        text=True,
        cwd=scratch,
        check=False,
        env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"},
    )
    outputs[lab] = proc.stdout
    print(f"twin {lab}: exit={proc.returncode} stderr_bytes={len(proc.stderr)} stdout_lines={proc.stdout.count(chr(10))}")

part_a_lines = outputs["L04"].split("Part A", 1)[1].split("Part B", 1)[0].splitlines()
rows = [re.split(r"\s+", line.strip()) for line in part_a_lines if re.match(r"^\s*\d+\s+\d+\s+-?\d+\s+-?\d+\s+[01]\s*$", line)]
assert len(rows) == 24, len(rows)
errors = [int(r[3]) for r in rows]
consistent = all(int(r[1]) - int(r[2]) == int(r[3]) and (abs(int(r[3])) <= 2) == (r[4] == "1") for r in rows)
hits = sum(int(r[4]) for r in rows)
bias = Fraction(sum(errors), 24)
mae = Fraction(sum(abs(e) for e in errors), 24)


def display(x: Fraction) -> str:
    sign = 1 if x >= 0 else -1
    return f"{sign * math.floor(abs(x) * 10**4 + Fraction(1, 2)) / 10**4:.4f}"


print(f"L04 Part A: rows={len(rows)} error=forecast-realised and hit rule consistent={consistent}")
print(f"  hits={hits} hit_rate={Fraction(hits, 24)} display={display(Fraction(hits, 24))}")
print(f"  sum_errors={sum(errors)} bias={bias} display={display(bias)} mae={mae}")

count = sum(1 for v in range(-4, 5) for u in range(-6, 7) if -3 <= v - u <= 1)
print(f"Prop 4.4: pairs=117 hit_pairs={count} P(hit)={Fraction(count, 117)} display={display(Fraction(count, 117))}")
print("  E[e] = 1 + E[V] - E[U] with E[V] = E[U] = 0 (symmetric ranges), so E[e] = 1")

src = (twins / "lab-LX2-L02-1.py").read_text(encoding="utf-8")
marker = src.index('label="P7"')
flag = src.index("source_told_of_trade=True", marker)
(scratch / "e3_copy.py").write_text(src[:flag] + "source_told_of_trade=False" + src[flag + len("source_told_of_trade=True"):], encoding="utf-8")
e3 = subprocess.run([sys.executable, "-I", "-W", "error", str(scratch / "e3_copy.py")], capture_output=True, text=True, cwd=scratch, check=False)
print("L02 E3 copy (P7 source-told False), summary lines:")
for line in e3.stdout.splitlines():
    if line.startswith(("fired:", "not fired:", "P7 ")):
        print("  " + line)
print("L03 flagged-traders line:", [line for line in outputs["L03"].splitlines() if line.startswith("traders flagged")])
state_rows = [line.split() for line in outputs["L01"].splitlines() if line.split()[:1] and line.split()[0] in ("unregistered", "filed", "refused", "effective", "stop_order") and len(line.split()) == 7]
print("L01 state rows with sale=yes:", [f"{r[0]}/{r[1]}" for r in state_rows if r[-1] == "yes"])
cards = json.loads((root / "course/modules/LX/LX2/cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards), "LX2-c100 back:", next(c["back"] for c in cards if c["id"] == "LX2-c100"))
