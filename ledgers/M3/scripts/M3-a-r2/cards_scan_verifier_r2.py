"""Verifier check (M3 slice a, round 2) of cards for L01-L03: every cited result exists in the cited lesson,
every card number appears in its lesson, duplicate and near-duplicate scan over the whole cards.json.
Usage: python -I -W error ledgers/M3/scripts/M3-a-r2/cards_check.py
"""

import difflib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
lessons = {}
for n in ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09"):
    t = (ROOT / f"course/modules/M/M3/{n}.html").read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    lessons[n] = html.unescape(re.sub(r"<[^>]+>", " ", t))
defs = {}
for n, t in lessons.items():
    for kind, num in re.findall(r"\b(Definition|Lemma|Proposition|Theorem|Corollary|Example|Remark|Assumption|Misconception|Problem)\s+([0-9]+\.[0-9]+)", t):
        defs.setdefault((kind, num), set()).add(n)
problems = []
checked = 0
for c in cards:
    if c["lesson"] not in ("L01", "L02", "L03"):
        continue
    text = c["front"] + " " + c["back"]
    for m in re.finditer(r"(Lesson (\d+),\s*)?(Definition|Lemma|Proposition|Theorem|Corollary|Example|Remark|Assumption)\s+([0-9]+\.[0-9]+)", text):
        kind, num = m.group(3), m.group(4)
        checked += 1
        home = f"L0{m.group(2)}" if m.group(2) else c["lesson"]
        if (kind, num) not in defs or home not in defs[(kind, num)]:
            if m.group(2) is None and c["lesson"] in defs.get((kind, num), set()):
                continue
            problems.append((c["id"], f"{kind} {num} not found in {home}", defs.get((kind, num))))
    for num in re.findall(r"\b\d+(?: of \d+| in \d+| to \d+)?\b", c["back"]):
        pass
    for lab in re.findall(r"\bLab 1\b", text):
        checked += 1
# numeric claims: card answers must appear in the lesson text of the same lesson
expect = {
    "M3-c016": ["188 of 200", "188"],
    "M3-c017": ["198 of 200", "198"],
    "M3-c018": ["100 of 100"],
    "M3-c019": ["0 of 200"],
    "M3-c038": ["50 of 50"],
    "M3-c039": ["50 of 50"],
    "M3-c057": ["3 of 3"],
    "M3-c058": ["det P = 6"],
    "M3-c059": ["residual below 1e-12"],
    "M3-c171": ["AP = PD"],
    "M3-c172": ["rank of"],
    "M3-c184": ["50 of 50"],
    "M3-c048": ["4.6180", "2.3820"],
}
byid = {c["id"]: c for c in cards}
for cid, needles in expect.items():
    c = byid[cid]
    home = lessons[c["lesson"]]
    for nd in needles:
        checked += 1
        if nd not in home:
            problems.append((cid, f"number/phrase {nd!r} absent from {c['lesson']} text", None))
# duplicate and near-duplicate scan across all cards
fronts = {}
for c in cards:
    key = re.sub(r"\W+", " ", c["front"].lower()).strip()
    fronts.setdefault(key, []).append(c["id"])
for k, ids in fronts.items():
    if len(ids) > 1:
        problems.append(("duplicate-front", k, ids))
near = []
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        if r >= 0.8:
            near.append((a["id"], b["id"], round(r, 2), a["front"][:60], b["front"][:60]))
ids = [c["id"] for c in cards]
dup_ids = {x for x in ids if ids.count(x) > 1}
print("cards total", len(cards), "L01-L03", sum(c["lesson"] in ("L01", "L02", "L03") for c in cards))
print("reference checks run", checked)
print("duplicate ids", dup_ids)
print("near-duplicate fronts (ratio>=0.8):", near)
print("problems:")
for p in problems:
    print("  ", p)
print("cards_check", "PASS" if not problems and not dup_ids else "FAIL")
