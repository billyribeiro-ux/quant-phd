import json, re, collections, sys
c = json.load(open(sys.argv[1], encoding="utf-8"))
cs = c if isinstance(c, list) else c.get("cards", c)
print("n cards", len(cs), "ids unique", len({x["id"] for x in cs}) == len(cs))
fr = collections.Counter(x["front"].strip().lower() for x in cs)
print("dup fronts", [k for k, v in fr.items() if v > 1])
for x in cs:
    if re.search(r"R\*|R_BE|threshold", x["front"] + " " + x["back"]):
        print("symbol", x["id"], x["lesson"])
