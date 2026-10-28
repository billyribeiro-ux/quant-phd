# Full card scan for M1 (round 18, M1-b): duplicate ids, duplicate fronts, grade/basis consistency, L04/L05 card list.
import json, sys
c = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [x["id"] for x in c]
fr = [x["front"] for x in c]
print("cards", len(c), "dup ids", len(ids) - len(set(ids)), "dup fronts", len(fr) - len(set(fr)))
bad = [x["id"] for x in c if x.get("grade") == "T" and x.get("basis")] + [
    x["id"] for x in c if x.get("grade") not in ("T", None) and not x.get("basis")]
print("grade/basis inconsistent:", bad)
for x in c:
    if x["lesson"] in ("L04", "L05"):
        print("LIST", x["id"], x["lesson"], x.get("grade"), "|", x["front"], "|", x["back"])
