"""Card checks for CS2 slice d, round 7: schema, ids, lesson links, numbers vs lesson text and lab output, duplicates."""
import difflib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
CS2 = ROOT / "course/modules/CS/CS2"
cards = json.loads((CS2 / "cards.json").read_text(encoding="utf-8"))
print("cards", len(cards))
ids = [c["id"] for c in cards]
assert len(set(ids)) == len(ids), "duplicate ids"
print("ids unique; all match CS2-cNNN:", all(re.fullmatch(r"CS2-c\d{3}", i) for i in ids))
keys_ok = all(set(c) == {"id", "lesson", "front", "back", "grade"} | ({"basis"} if c["grade"] != "T" else set()) for c in cards)
print("schema keys ok:", keys_ok, "(basis present exactly when grade != T)")
print("grades:", sorted({c["grade"] for c in cards}))
print("lessons used:", sorted({c["lesson"] for c in cards}))
lessons = {}
for L in sorted({c["lesson"] for c in cards}):
    raw = (CS2 / f"{L}.html").read_text(encoding="utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)))
    text = re.sub(r"\s+", " ", text)
    lessons[L] = (raw, text)
missing_lessons = [L for L in range(1, 12) if f"L{L:02d}" not in lessons]
print("lessons with no cards:", [f"L{L:02d}" for L in range(1, 12) if f"L{L:02d}" not in lessons])
# every lesson has at least one card
# numbers in back and front must appear in lesson text (after normalising)
NUM = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:e-?\d+)?")
bad = []
for c in cards:
    text = lessons[c["lesson"]][1]
    for s in ("front", "back"):
        for num in set(NUM.findall(c[s])):
            if num in ("0", "1", "2"):
                continue
            if num not in text:
                bad.append((c["id"], s, num))
print("numbers (other than 0,1,2) on a card missing from its lesson text:", len(bad))
for b in bad:
    print("   ", b)
# definitions/propositions cited on card back must exist in the lesson
REF = re.compile(r"\((Definition|Proposition|Theorem|Corollary|Lemma|Remark|Problem|Example|Assumption|Section|Misconception|Lab|Model)[^)]*\)")
for c in cards:
    for ref in re.findall(r"\(((?:Definition|Proposition|Theorem|Corollary|Lemma|Remark|Problem|Example|Assumption|Misconception)s? [0-9][^)]*)\)", c["back"]):
        label = re.match(r"(Definition|Proposition|Theorem|Corollary|Lemma|Remark|Problem|Example|Assumption|Misconception)s? (\d\.\d+|P\d+|R\d+|E\d+|M\d+|\d+)", ref)
        if label:
            kind, num = label.group(1), label.group(2)
            pat = {"Problem": f"Problem {num}", "Misconception": "Misconception", }.get(kind, f"{kind} {num}")
            if pat not in lessons[c["lesson"]][1]:
                print("   reference not found in lesson:", c["id"], repr(ref))
print("done reference scan")
# lab numbers: run the lesson twin and check each number printed on a grade C card is in its output or lesson text
twins = {}
for L in lessons:
    tw = ROOT / f"tests/labs/CS2/lab-CS2-{L}-1.py"
    if tw.exists():
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(tw)], capture_output=True, text=True, cwd="/tmp/cs2r7")
        twins[L] = r.stdout + r.stderr
        print(f"twin {L}: exit {r.returncode}")
    else:
        print("no twin", L)
odd = []
for c in cards:
    if c["grade"] == "C":
        out = twins.get(c["lesson"], "")
        for num in set(NUM.findall(c["back"])):
            if num in ("0", "1", "2"):
                continue
            if num not in out and num not in lessons[c["lesson"]][1]:
                odd.append((c["id"], num))
print("grade C numbers not in twin output or lesson text:", len(odd))
for o in odd:
    print("   ", o)
# duplicates: exact front/back and near-duplicate fronts
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
seen = {}
for c in cards:
    k = norm(c["front"])
    if k in seen:
        print("EXACT DUPLICATE FRONT", c["id"], seen[k])
    seen[k] = c["id"]
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        fr = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        bk = difflib.SequenceMatcher(None, norm(a["back"]), norm(b["back"])).ratio()
        if fr > 0.8 or bk > 0.8:
            pairs.append((round(fr, 2), round(bk, 2), a["id"], b["id"]))
print("near-duplicate pairs (front>0.8 or back>0.8):", len(pairs))
for p in pairs:
    print("   ", p)
