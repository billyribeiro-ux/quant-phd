import json, sys
def load(p):
    d = json.load(open(p, encoding="utf-8"))
    cards = d if isinstance(d, list) else d.get("cards", d)
    return {c["id"]: c for c in cards}
base = load(sys.argv[1]); head = load(sys.argv[2])
ids = sys.argv[3].split(",")
for i in ids:
    b, h = base.get(i), head.get(i)
    if b == h:
        print(i, "IDENTICAL"); continue
    print("==", i)
    for k in sorted(set(b or {}) | set(h or {})):
        if (b or {}).get(k) != (h or {}).get(k):
            print("  field", k)
            print("    base:", json.dumps((b or {}).get(k), ensure_ascii=False)[:700])
            print("    head:", json.dumps((h or {}).get(k), ensure_ascii=False)[:700])
