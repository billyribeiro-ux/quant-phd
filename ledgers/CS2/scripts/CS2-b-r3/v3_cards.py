"""Card checks for CS2 slice b (cards with lesson L05-L08), run from the checkout root.

Usage: python -I -W error v3_cards.py   (standard library only; writes nothing)
Checks: count by lesson; every card has a valid grade; every C card has a basis; every card number
(digit groups of two or more digits, plus decimals) appears in its lesson text; ids unique; the
delta against the previous pin 9294b914 (ids added, removed, changed).
"""

import difflib
import html
import json
import re
import subprocess
from collections import Counter

ROOT = "."
SLICE = ("L05", "L06", "L07", "L08")


def lesson_text(page: str) -> str:
    with open(f"course/modules/CS/CS2/{page}.html", encoding="utf-8") as fh:
        raw = fh.read()
    return html.unescape(re.sub(r"<[^>]+>", " ", raw)).replace("\\", "")


def load(text: str) -> list[dict]:
    return json.loads(text)


def main() -> None:
    with open("course/modules/CS/CS2/cards.json", encoding="utf-8") as fh:
        cards = load(fh.read())
    ids = [c["id"] for c in cards]
    print(f"total cards {len(cards)}; duplicate ids {len(ids) - len(set(ids))}")
    sl = [c for c in cards if c["lesson"] in SLICE]
    print(f"slice cards {len(sl)} by lesson {dict(Counter(c['lesson'] for c in sl))}")
    print(f"grades {dict(Counter(c['grade'] for c in sl))}")
    bad_grade = [c["id"] for c in sl if c["grade"] not in {"T", "A", "B", "C", "D", "X"}]
    no_basis = [c["id"] for c in sl if c["grade"] == "C" and not c.get("basis")]
    print(f"bad grade {bad_grade}; C cards without basis {no_basis}")
    texts = {p: lesson_text(p) for p in SLICE}
    missing = []
    for c in sl:
        text = texts[c["lesson"]]
        nums = set(re.findall(r"\d+(?:\.\d+)?", c["back"] + " " + c["front"]))
        for n in sorted(nums):
            if n in {"1", "2", "0"}:
                continue
            if n not in text.replace(",", "").replace(" ", "") and n not in text:
                missing.append((c["id"], n))
    print(f"numbers in card text absent from own lesson (excluding 0,1,2): {missing}")
    print("near-duplicate pairs within slice (back similarity >= 0.6 or front >= 0.8):")
    for i, a in enumerate(sl):
        for b in sl[i + 1 :]:
            rf = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
            rb = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
            if rb >= 0.6 or rf >= 0.8:
                print(f"  {a['id']} / {b['id']}: front {rf:.2f} back {rb:.2f}")
    old = {c["id"]: c for c in load(subprocess.run(
        ["git", "show", "9294b914:course/modules/CS/CS2/cards.json"], capture_output=True, text=True,
        check=True).stdout)}
    new = {c["id"]: c for c in cards}
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(i for i in set(new) & set(old) if new[i] != old[i])
    print(f"delta vs 9294b914: added {[(i, new[i]['lesson']) for i in added]}")
    print(f"delta vs 9294b914: removed {[(i, old[i]['lesson']) for i in removed]}")
    print(f"delta vs 9294b914: changed {[(i, new[i]['lesson']) for i in changed]}")


main()
