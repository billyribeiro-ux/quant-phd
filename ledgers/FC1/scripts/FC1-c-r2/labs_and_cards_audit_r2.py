"""Structural audit for FC1 slice c (round 2): page lab code vs twin, page expected block vs run, card ids, duplicates, grades.

Run from the checkout root: .venv/bin/python -I ledgers/FC1/scripts/FC1-c-r2/labs_and_cards_audit_r2.py
"""

import difflib
import html
import itertools
import json
import re
import subprocess
import sys

ROOT = "."
src = open(f"{ROOT}/course/modules/FC/FC1/project.html", encoding="utf-8").read()
blocks = re.findall(
    r'<section class="lab[^"]*" id="(lab-FC1-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>',
    src,
    re.S,
)
expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
for (lab, code), exp in zip(blocks, expected):
    page = html.unescape(code).rstrip("\n")
    twin = open(f"{ROOT}/tests/labs/FC1/{lab}.py", encoding="utf-8").read().rstrip("\n")
    diff = [d for d in difflib.unified_diff(twin.splitlines(), page.splitlines(), lineterm="", n=0) if d[:1] in "+-" and d[:3] not in ("+++", "---")]
    run = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/FC1/{lab}.py"], capture_output=True, text=True).stdout
    print(lab, "page vs twin differing lines:", len(diff) // 2 if diff else 0, "| expected == run:", html.unescape(exp).strip() == run.strip())

cards = json.load(open(f"{ROOT}/course/modules/FC/FC1/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique", len(set(ids)), "sequential", ids == [f"FC1-c{i:03d}" for i in range(1, len(cards) + 1)])
print("duplicate fronts", [f for f in {c["front"] for c in cards} if sum(c["front"] == f for c in cards) > 1])
close = [(a["id"], b["id"], round(difflib.SequenceMatcher(None, a["front"], b["front"]).ratio(), 2)) for a, b in itertools.combinations(cards, 2)]
print("front pairs with similarity >= 0.8:", [c for c in close if c[2] >= 0.8])
print("grade counts", {g: sum(1 for c in cards if c.get("grade") == g) for g in "TCABDX"}, "no grade field:", sum(1 for c in cards if "grade" not in c))
print("cards with grade C:", [c["id"] for c in cards if c.get("grade") == "C"])
print("cards with grade T:", [c["id"] for c in cards if c.get("grade") == "T"])
