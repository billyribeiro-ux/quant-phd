"""Verifier scan (M3 slice a, round 2): banned strings of BUILDER_RULES 1.3-1.4 and process words in the hub, L01-L03, their twins and the L01-L03 cards.
Usage: python -I -W error ledgers/M3/scripts/M3-a-r2/banned_scan_r2.py   (run from the checkout root; reads only repository files)
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BANNED = [
    "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
    "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
    "obviously", "clearly", "in conclusion", "let's", "let us", "great question", "rhetorical",
    "architect", "builder", "verifier", "orchestrat", "planner", "REQUEST", "DAG_DEFECT", "ledger", "round 1", "round 2",
    "agent", "fanout", "workflow", "in summary", "to summarize", "as we saw", "hope this helps",
]
files = [ROOT / "course/modules/M/M3/index.html"] + [ROOT / f"course/modules/M/M3/L0{i}.html" for i in (1, 2, 3)]
files += [ROOT / "tests/labs/M3/lab-M3-L01-1.py", ROOT / "tests/labs/M3/lab-M3-L02-1.py", ROOT / "tests/labs/M3/lab-M3-L03-1.py"]
hits = 0
for f in files:
    raw = f.read_text(encoding="utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw)) if f.suffix == ".html" else raw
    for word in BANNED:
        for m in re.finditer(re.escape(word), text, re.I):
            hits += 1
            line = text.count("\n", 0, m.start()) + 1
            print(f"HIT {f.relative_to(ROOT)}:{line} {word!r}: {text[max(0,m.start()-40):m.end()+40]!r}")
cards = json.loads((ROOT / "course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03"):
        s = c["front"] + " " + c["back"]
        for word in BANNED:
            if re.search(re.escape(word), s, re.I):
                hits += 1
                print(f"HIT cards {c['id']} {word!r}")
print("banned/process-word hits:", hits)
