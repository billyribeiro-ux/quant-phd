import json, re, itertools
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))
def jac(a, b):
    return len(a & b) / max(1, len(a | b))
print("cards:", len(cards), "unique ids:", len({c['id'] for c in cards}))
print("unique fronts:", len({c['front'] for c in cards}), "unique backs:", len({c['back'] for c in cards}))
pairs = []
for a, b in itertools.combinations(cards, 2):
    fa, fb = toks(a["front"]), toks(b["front"])
    ba, bb = toks(a["back"]), toks(b["back"])
    sf, sb = jac(fa, fb), jac(ba, bb)
    if sf >= 0.5 or sb >= 0.6:
        pairs.append((round(sf, 2), round(sb, 2), a["id"], a["lesson"], b["id"], b["lesson"]))
for p in sorted(pairs, reverse=True):
    print(p)
print("pairs flagged:", len(pairs))
