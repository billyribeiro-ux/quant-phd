"""Closing-delta banned-string and process-word scan (M3 slice a, round 1).

Scans the L01-L03 cards of cards.json (whole text) and the hub, L01-L03 pages (visible text) and the L01-L03 twins.
Run: python -I -W error ledgers/M3/scripts/M3-a-r1/banned_scan_r1.py  (repository files only)
"""
import html
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M3-a")
BANNED = [
    "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
    "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
    "obviously", "clearly", "in conclusion", "let's", "let us", "great question", "rhetorical",
    "architect", "builder", "verifier", "orchestrat", "planner", "REQUEST", "DAG_DEFECT", "ledger", "round 1", "round 2",
    "agent", "fanout", "workflow", "in summary", "to summarize", "as we saw", "hope this helps", "ruling", "fixer",
]
hits = 0
files = [ROOT / "course/modules/M/M3/index.html"] + [ROOT / f"course/modules/M/M3/L0{i}.html" for i in (1, 2, 3)]
files += [ROOT / f"tests/labs/M3/lab-M3-L0{i}-1.py" for i in (1, 2, 3)]
for f in files:
    raw = f.read_text(encoding="utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw)) if f.suffix == ".html" else raw
    for word in BANNED:
        for m in re.finditer(re.escape(word), text, re.I):
            hits += 1
            print(f"HIT {f.relative_to(ROOT)} {word!r}: {text[max(0, m.start() - 40):m.end() + 40]!r}")
cards = json.loads((ROOT / "course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
n = 0
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03"):
        n += 1
        s = c["front"] + " " + c["back"]
        for word in BANNED:
            if re.search(re.escape(word), s, re.I):
                hits += 1
                print(f"HIT cards {c['id']} {word!r}")
print("L01-L03 cards scanned", n, "banned/process-word hits:", hits)
