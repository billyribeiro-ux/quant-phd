"""Round-10 verifier D: full structural scan of course/modules/M/M4/cards.json.

Checks: JSON parses; every card has id, lesson, front, back, grade; ids unique and of the form M4-cNNN; lesson in L01..L10;
every lesson has at least one card; grade in {T, A, B, C, D, X}; a non-T card has a cite or a basis; cite only the registry key
blitzstein2019introduction (and that key exists in references/references.json); no exact or case-normalised duplicate front or
back; every integer or decimal token in a card's front or back appears in the lesson the card cites (after stripping tags);
and the list of cards with a basis that names a lab. Prints counts and any failing card ids."""

import html
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD10-M4-d")
M4 = ROOT / "course/modules/M/M4"
cards = json.loads((M4 / "cards.json").read_text(encoding="utf-8"))
registry = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
keys = {r.get("key") for r in registry} if isinstance(registry, list) else set(registry.keys())
problems = []
ids = Counter(c.get("id") for c in cards)
print("cards:", len(cards), "unique ids:", len(ids), "duplicated ids:", [i for i, n in ids.items() if n > 1])
lessons = Counter(c["lesson"] for c in cards)
print("per lesson:", dict(sorted(lessons.items())))
for L in [f"L{n:02d}" for n in range(1, 11)]:
    if lessons.get(L, 0) == 0:
        problems.append(f"no card for {L}")
grades = Counter(c["grade"] for c in cards)
print("grades:", dict(grades))
keyset = {"id", "lesson", "front", "back", "grade", "cite", "basis"}
extra_keys = Counter(k for c in cards for k in c if k not in {"id", "lesson", "front", "back", "grade"})
print("optional keys:", dict(extra_keys))
for c in cards:
    cid = c["id"]
    if not re.fullmatch(r"M4-c\d{3}", cid):
        problems.append(f"{cid}: bad id")
    if set(c) - keyset:
        problems.append(f"{cid}: unexpected keys {sorted(set(c) - keyset)}")
    if c["lesson"] not in lessons or not re.fullmatch(r"L(0[1-9]|10)", c["lesson"]):
        problems.append(f"{cid}: bad lesson {c['lesson']}")
    if c["grade"] not in {"T", "A", "B", "C", "D", "X"}:
        problems.append(f"{cid}: bad grade {c['grade']}")
    if c["grade"] != "T" and not (c.get("cite") or c.get("basis")):
        problems.append(f"{cid}: non-T without cite or basis")
    if c.get("cite") and c["cite"] != "blitzstein2019introduction":
        problems.append(f"{cid}: cite {c['cite']} is not the M4 registry key")
    if c.get("cite") and c["cite"] not in keys:
        problems.append(f"{cid}: cite not in registry")
    if c.get("basis") and not str(c["basis"]).strip():
        problems.append(f"{cid}: empty basis")
    if not c["front"].strip() or not c["back"].strip():
        problems.append(f"{cid}: empty front or back")
norm_front = defaultdict(list)
norm_back = defaultdict(list)
for c in cards:
    norm_front[re.sub(r"\W+", " ", c["front"].lower()).strip()].append(c["id"])
    norm_back[re.sub(r"\W+", " ", c["back"].lower()).strip()].append(c["id"])
for k, v in norm_front.items():
    if len(v) > 1:
        problems.append(f"duplicate front {v}")
for k, v in norm_back.items():
    if len(v) > 1:
        problems.append(f"duplicate back {v}")
# numbers in the card must appear in the cited lesson
def lesson_text(L: str) -> str:
    raw = (M4 / f"{L}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))
texts = {L: lesson_text(L) for L in lessons}
missing_numbers = []
for c in cards:
    body = c["front"] + " " + c["back"]
    for tok in set(re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?", body)):
        if tok not in texts[c["lesson"]]:
            missing_numbers.append((c["id"], tok))
print("card number tokens absent from the card's lesson:", missing_numbers)
print("problems:", len(problems))
for p in problems:
    print("  ", p)
lab_basis = [c["id"] for c in cards if c.get("basis") and "Lab" in c["basis"]]
print("cards whose basis names a lab:", len(lab_basis))
sys.stdout.flush()
