import json, sys
cards = json.load(open(sys.argv[1]))
for c in cards:
    if c.get("lesson") in sys.argv[2].split(","):
        print(f'{c["id"]} {c["lesson"]} grade={c.get("grade")} basis={c.get("basis")!r} cite={c.get("cite")!r}')
        print("  F:", c["front"])
        print("  B:", c["back"])
        extra = {k: v for k, v in c.items() if k not in ("id","lesson","front","back","grade","basis","cite")}
        if extra: print("  EXTRA:", extra)
