"""Slice-b card checks: id/lesson placement, numbers on each card present in its lesson, near-duplicate scan."""
import json, re, html, difflib, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS4-M2-b")
cards = json.loads((ROOT / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)), "unique fronts", len({c["front"] for c in cards}))
dups = [i for i in set(ids) if ids.count(i) > 1]
print("duplicate ids", dups)
SLICE = ("L07", "L08", "L09", "L10", "L11", "L12")
slice_cards = [c for c in cards if c["lesson"] in SLICE]
print("slice-b cards", len(slice_cards), {L: sum(1 for c in slice_cards if c["lesson"] == L) for L in SLICE})
def page_text(L):
    raw = (ROOT / f"course/modules/M/M2/{L}.html").read_text(encoding="utf-8")
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))
texts = {L: page_text(L) for L in SLICE}
# numbers on each card (tokens with a digit) must appear in the card's own lesson page
missing = []
for c in slice_cards:
    body = c["front"] + " " + c["back"]
    for tok in set(re.findall(r"\d[\d.,/^\-e]*\d|\d", body)):
        tok_clean = tok.rstrip(".,")
        if tok_clean and tok_clean not in texts[c["lesson"]]:
            missing.append((c["id"], c["lesson"], tok_clean))
print("numbers not found in own lesson page:", len(missing))
for m in missing:
    print("  ", m)
# near-duplicates: slice card fronts vs all other cards (similarity >= 0.75)
pairs = []
for a in slice_cards:
    for b in cards:
        if b["id"] == a["id"]:
            continue
        r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        if r >= 0.75:
            pairs.append((round(r, 2), a["id"], a["lesson"], b["id"], b["lesson"], a["front"][:70], b["front"][:70]))
print("front-similarity >= 0.75 pairs involving slice-b cards:", len(pairs))
for p in sorted(pairs, reverse=True):
    print("  ", p)
# back-text similarity among slice cards vs all
bpairs = []
for a in slice_cards:
    for b in cards:
        if b["id"] == a["id"]:
            continue
        r = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
        if r >= 0.7:
            bpairs.append((round(r, 2), a["id"], a["lesson"], b["id"], b["lesson"], a["back"][:60], b["back"][:60]))
print("back-similarity >= 0.70 pairs involving slice-b cards:", len(bpairs))
for p in sorted(bpairs, reverse=True):
    print("  ", p)
# grades and basis for slice-b cards
import collections
print("grades", collections.Counter((c["lesson"], c.get("grade")) for c in slice_cards))
print("cards with grade C:", [(c["id"], c.get("basis")) for c in slice_cards if c.get("grade") == "C"])
print("cards with grade T but basis set:", [(c["id"], c.get("basis")) for c in slice_cards if c.get("grade") == "T" and c.get("basis")])
