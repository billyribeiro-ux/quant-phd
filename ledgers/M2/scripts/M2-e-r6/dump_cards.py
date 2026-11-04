import json, sys
cards = json.load(open(sys.argv[1]))
want = set(sys.argv[2].split(','))
for c in cards:
    if c['lesson'] in want:
        extra = {k: v for k, v in c.items() if k not in ('id', 'lesson', 'front', 'back')}
        print(f"{c['id']} {c['lesson']} {extra}")
        print("  F:", c['front'])
        print("  B:", c['back'])
