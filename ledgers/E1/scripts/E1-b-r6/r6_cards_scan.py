"""Round-6 card scan for E1 (verifier-written). Reads cards.json at the checkout and at the round-5 pin."""
import html
import itertools
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OLD_PIN = "dde0486b"
LESSONS = {"L04", "L05", "L06"}
base = ROOT / "course/modules/E/E1"


def plain(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    return re.sub(r"\s+", " ", raw)


def old_cards() -> list:
    out = subprocess.run(
        ["git", "show", f"{OLD_PIN}:course/modules/E/E1/cards.json"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    return json.loads(out)


cards = json.loads((base / "cards.json").read_text(encoding="utf-8"))
old = {c["id"]: c for c in old_cards()}
new = {c["id"]: c for c in cards}
pages = {L: plain(base / f"{L}.html") for L in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09"]}

print("cards total:", len(cards), "ids unique:", len(new) == len(cards))
removed = sorted(set(old) - set(new))
added = sorted(set(new) - set(old))
changed = sorted(i for i in set(old) & set(new) if old[i] != new[i])
print("removed:", removed)
print("added:", added)
print("changed:", changed)

NUM = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?")
CITE = re.compile(r"\b(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example|Assumption|Problem|Lab) (\d+(?:\.\d+)?)\b")

bad = 0
for c in cards:
    text = c["front"] + " " + c["back"]
    lesson = c["lesson"]
    src = pages.get(lesson, "")
    miss_num = [t for t in set(NUM.findall(text)) if t not in src]
    miss_cite = []
    for kind, num in CITE.findall(text):
        # Cross-lesson citations ("of Lesson 6") are checked against the cited lesson
        m = re.search(rf"{kind} {re.escape(num)} of Lesson (\d)", text)
        target = f"L0{m.group(1)}" if m else lesson
        if m is None and re.search(rf"{kind} {re.escape(num)}\b", text) and False:
            pass
        if f"{kind} {num}" not in pages.get(target, ""):
            miss_cite.append(f"{kind} {num} not in {target}")
    if miss_num or miss_cite:
        bad += 1
        print("MISS", c["id"], lesson, "numbers:", miss_num, "cites:", miss_cite)
print("cards with misses:", bad)

# duplicate scan: normalised fronts, and pairwise token similarity of fronts+backs within the same lesson
def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

fronts = {}
for c in cards:
    fronts.setdefault(norm(c["front"]), []).append(c["id"])
print("duplicate normalised fronts:", [v for v in fronts.values() if len(v) > 1])

def toks(c: dict) -> set:
    return set(re.findall(r"[a-z0-9]+", (c["front"] + " " + c["back"]).lower()))

pairs = []
for a, b in itertools.combinations(cards, 2):
    ta, tb = toks(a), toks(b)
    j = len(ta & tb) / max(1, len(ta | tb))
    if j >= 0.45:
        pairs.append((round(j, 2), a["id"], b["id"], a["lesson"], b["lesson"]))
for p in sorted(pairs, reverse=True):
    print("SIM", p)

# numeric answer collisions: same reference-case values on two cards
for key in ["200/3", "20000/9", "2222", "1111", "10000/9", "2500", "100/3"]:
    ids = [c["id"] for c in cards if key in c["front"] + c["back"]]
    print("token", key, ids)
