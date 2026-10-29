"""E5 slice d r3: every number on a card must appear in its lesson page text (or in its lesson's lab outputs). Also duplicate scan and id/lesson checks.
Usage: python3 -I card_numbers_in_lesson.py <repo-root>"""
import json, re, sys, html, collections, glob
from pathlib import Path
root = Path(sys.argv[1]); mod = root / "course/modules/E/E5"
cards = json.load(open(mod / "cards.json", encoding="utf-8"))
def text_of(p):
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s)
lesson_text = {}
for L in sorted(glob.glob(str(mod / "L0*.html"))):
    lesson_text[Path(L).stem] = text_of(L)
labs = {}
for f in sorted(glob.glob(str(root / "tests/labs/E5/*.py"))):
    labs[Path(f).stem] = None
# outputs: run twins in scratch dir not needed: use expected blocks from the lesson pages instead (run_labs checks equality)
ids = collections.Counter(c["id"] for c in cards)
print("CARDS", len(cards), "unique ids", len(ids), "dup ids", [k for k, v in ids.items() if v > 1])
print("LESSON COUNTS", collections.Counter(c["lesson"] for c in cards))
seq_ok = all(c["id"] == f"E5-c{i+1:03d}" for i, c in enumerate(cards))
print("ID SEQUENCE CONTIGUOUS", seq_ok)
num_re = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?:/\d+)?(?![\w])")
missing = []
for c in cards:
    lt = lesson_text.get(c["lesson"], "")
    body = c["front"] + " " + c["back"]
    for tok in set(num_re.findall(body)):
        t = tok.lstrip("-")
        if re.fullmatch(r"\d+", t) and int(t) <= 3 and c["lesson"] not in ("",):
            pass  # small integers (e.g., 0, 1, 2, 3) occur everywhere; checked by eye
        if t in lt or tok in lt:
            continue
        missing.append((c["id"], c["lesson"], tok))
print("NUMBERS NOT FOUND IN OWN LESSON TEXT (incl. small ints):", len(missing))
for m in missing:
    print("  ", m)
# duplicate scan: normalised fronts
norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
fr = collections.defaultdict(list)
for c in cards:
    fr[norm(c["front"])].append(c["id"])
print("DUPLICATE FRONTS", {k: v for k, v in fr.items() if len(v) > 1})
