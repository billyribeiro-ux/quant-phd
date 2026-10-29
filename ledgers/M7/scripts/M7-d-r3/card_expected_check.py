"""For each C card of M7, list the numbers in its back that do not appear in its lesson's expected (printed) lab output."""
import html
import json
import re
import sys
from pathlib import Path

base = Path(sys.argv[1])
cards = json.loads((base / "cards.json").read_text(encoding="utf-8"))
exp = {}
for lesson in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"]:
    s = (base / f"{lesson}.html").read_text(encoding="utf-8")
    blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', s, flags=re.S)
    exp[lesson] = html.unescape(" ".join(re.sub(r"<[^>]+>", "", b) for b in blocks))
pat = re.compile(r"\d+(?:/\d+)?(?:\.\d+)?")
for c in cards:
    if c["grade"] != "C":
        continue
    nums = [n for n in pat.findall(c["back"]) if n not in ("0", "1", "2", "3", "4", "5", "6")]
    print(c["id"], c["lesson"], "not-in-expected:", [n for n in nums if n not in exp[c["lesson"]]])
