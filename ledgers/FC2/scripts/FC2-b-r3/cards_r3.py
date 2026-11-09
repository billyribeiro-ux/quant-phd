"""FC2 slice b round 3: card checks for L04-L06: schema, ids, lesson, numbers present in lesson, near-duplicate scan (whole deck)."""
import json, re, pathlib, itertools
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS3-FC2-b")
cards = json.loads((ROOT / "course/modules/FC/FC2/cards.json").read_text(encoding="utf-8"))
keys = {}
for c in cards:
    keys.setdefault(tuple(sorted(c.keys())), 0); keys[tuple(sorted(c.keys()))] += 1
print("key sets:", keys)
print("grade values:", sorted({str(c.get("grade")) for c in cards}))
print("ids unique:", len({c['id'] for c in cards}) == len(cards), "count", len(cards))
text = {}
for L in ["L04", "L05", "L06"]:
    raw = (ROOT / f"course/modules/FC/FC2/{L}.html").read_text(encoding="utf-8")
    txt = re.sub(r"<[^>]+>", " ", raw)
    import html as h
    text[L] = h.unescape(txt)
slice_cards = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("slice cards", len(slice_cards))
missing = []
for c in slice_cards:
    nums = set(re.findall(r"\d+(?:\.\d+)?", c["front"] + " " + c["back"]))
    for n in nums:
        if n in ("1", "0", "2", "3", "4", "5", "10"):  # trivial small numbers; still check presence below for exposure
            continue
        if n not in text[c["lesson"]]:
            missing.append((c["id"], n))
print("numbers (>=6 excluding trivial) not found verbatim in own lesson:", missing)
def toks(c):
    return set(re.findall(r"[a-z]{3,}", (c["front"] + " " + c["back"]).lower()))
pairs = []
for a, b in itertools.combinations(cards, 2):
    ta, tb = toks(a), toks(b)
    j = len(ta & tb) / max(1, len(ta | tb))
    if j >= 0.45:
        pairs.append((round(j, 2), a["id"], a["lesson"], b["id"], b["lesson"]))
for p in sorted(pairs, reverse=True)[:25]:
    print("near-dup", p)
fronts = {}
for c in cards:
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
print("exact duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
