import json, sys
cards = json.load(open(sys.argv[1], encoding="utf-8"))
want = set(sys.argv[2:])
for c in cards:
    if c["lesson"] in want:
        print(f'### {c["id"]} [{c["lesson"]}] keys={sorted(c.keys())}')
        print("FRONT: " + c["front"])
        print("BACK: " + c["back"])
