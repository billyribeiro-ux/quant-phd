import json, sys
cards = json.load(open(sys.argv[1], encoding="utf-8"))
for c in cards:
    if c["lesson"] in sys.argv[2:]:
        print(json.dumps(c, ensure_ascii=False))
