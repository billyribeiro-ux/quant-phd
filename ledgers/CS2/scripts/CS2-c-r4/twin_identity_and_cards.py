"""Verifier round 4: (1) each data-run block equals its twin and each expected block equals the twin's output,
(2) the 41 CS2 L09-L11 cards have id, lesson, front, back, grade and (for non-T) cite or basis.
Run from the checkout root: .venv/bin/python -I ledgers/CS2/scripts/CS2-c-r4/twin_identity_and_cards.py"""
import html
import json
import re
import subprocess
import sys

ROOT = "."
for L in ("L09", "L10", "L11"):
    s = open(f"{ROOT}/course/modules/CS/CS2/{L}.html", encoding="utf-8").read()
    twin = open(f"{ROOT}/tests/labs/CS2/lab-CS2-{L}-1.py", encoding="utf-8").read()
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', s, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S).group(1))
    out = subprocess.run([sys.executable, "-I", f"{ROOT}/tests/labs/CS2/lab-CS2-{L}-1.py"], capture_output=True, text=True).stdout
    print(L, "data-run==twin", code.strip() == twin.strip(), "expected==output", exp.strip() == out.strip())
cards = json.load(open(f"{ROOT}/course/modules/CS/CS2/cards.json", encoding="utf-8"))
sl = [c for c in cards if c["lesson"] in ("L09", "L10", "L11")]
print("L09-L11 cards:", len(sl), "first", sl[0]["id"], "last", sl[-1]["id"])
print("missing fields:", [c["id"] for c in sl if not all(k in c for k in ("id", "lesson", "front", "back", "grade"))])
print("non-T without cite/basis:", [c["id"] for c in sl if c["grade"] != "T" and not (c.get("cite") or c.get("basis"))])
