import json, sys
cards = json.load(open(sys.argv[1]))
if isinstance(cards, dict):
    cards = cards.get("cards", cards)
for c in cards:
    if c.get("lesson") in ("L05", "L06", "L07", "L08"):
        print(f'{c["id"]} {c.get("lesson")} grade={c.get("grade")} basis={c.get("basis","")!r}')
        print("  F:", c.get("front"))
        print("  B:", c.get("back"))
        print("  extra:", {k: v for k, v in c.items() if k not in ("id","lesson","front","back","grade","basis")})
