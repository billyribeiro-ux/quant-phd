"""Round-6 card checks for M5 L08-L10 (and unit-wide duplicate scan): schema, lesson agreement of numbers, banned and process words."""
import difflib
import html
import itertools
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/M/M5/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)), "duplicate ids:", [i for i, n in Counter(ids).items() if n > 1])
print("per lesson:", dict(sorted(Counter(c["lesson"] for c in cards).items())))
bad = [c["id"] for c in cards if not re.fullmatch(r"M5-c\d{3}", c["id"]) or not c.get("front") or not c.get("back")]
print("schema problems (id pattern, empty front/back):", bad)
print("graded cards without basis/cite:", [c["id"] for c in cards if c.get("grade") and not (c.get("basis") or c.get("cite"))])
print("grade values:", dict(Counter(c.get("grade") for c in cards)))

def page_text(path):
    t = (ROOT / path).read_text(encoding="utf-8")
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(t)
texts = {L: page_text(f"course/modules/M/M5/{L}.html") for L in ("L08", "L09", "L10")}
outs = {L: (ROOT / f"ledgers/M5/scripts/M5-c-r6/out/twin_{L}.stdout").read_text(encoding="utf-8") for L in ("L08", "L09", "L10")}
num_re = re.compile(r"\d+\.\d+(?:e[-+]?\d+)?|\d+/\d+|10\^\(?−\d+\)?|\b\d+\b")
print("== numeric tokens on L08-L10 cards not found verbatim in the lesson text or twin stdout")
for c in cards:
    if c["lesson"] not in texts:
        continue
    blob = c["front"] + " " + c["back"]
    toks = set(num_re.findall(blob))
    hay = texts[c["lesson"]] + " " + outs[c["lesson"]]
    miss = [t for t in toks if t not in hay and t.replace("−", "-") not in hay]
    if miss:
        print(c["id"], c["lesson"], miss)
print("== banned and process words in L08-L10 card text and in the three lesson texts (word hits)")
banned = re.compile(r"\b(TODO|TBD|lorem|omitted|beyond the scope|for brevity|clearly|obviously|well known|can be shown|roughly|it is important|previous|revis\w*|updat\w*|ledger|verif\w*|builder|agent|reviewer|earlier|ruling|audit|round)\b", re.I)
for c in cards:
    if c["lesson"] in texts:
        h = banned.findall(c["front"] + " " + c["back"])
        if h:
            print(c["id"], h)
for L, t in texts.items():
    hits = sorted(set(m.group(0).lower() for m in banned.finditer(t)))
    print(L, "word hits:", hits)
print("== near-duplicate pairs inside L08-L10 (combined similarity > 0.45, or front or back > 0.6)")
sub = [c for c in cards if c["lesson"] in ("L08", "L09", "L10")]
for a, b in itertools.combinations(sub, 2):
    r = difflib.SequenceMatcher(None, a["front"] + " " + a["back"], b["front"] + " " + b["back"], autojunk=False).ratio()
    fr = difflib.SequenceMatcher(None, a["front"], b["front"], autojunk=False).ratio()
    br = difflib.SequenceMatcher(None, a["back"], b["back"], autojunk=False).ratio()
    if r > 0.45 or fr > 0.6 or br > 0.6:
        print(f"{a['id']}({a['lesson']}) {b['id']}({b['lesson']}) combined={r:.2f} front={fr:.2f} back={br:.2f}")
