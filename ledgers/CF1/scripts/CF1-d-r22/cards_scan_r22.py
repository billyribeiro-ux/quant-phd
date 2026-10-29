"""Scan course/modules/CF/CF1/cards.json: fields, grades, basis, duplicates, banned and process words, numbers vs lessons."""
import json, re, collections, pathlib
root = pathlib.Path("/tmp/verify22-CF1-d/course/modules/CF/CF1")
cards = json.load(open(root / "cards.json"))
print("entries", len(cards), collections.Counter(c["grade"] for c in cards))
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets", {len(k): v for k, v in keys.items()})
bad = [c["id"] for c in cards if not c.get("basis") or c["grade"] not in ("T", "C")]
print("missing grade or basis", bad)
ids = collections.Counter(c["id"] for c in cards)
print("duplicate ids", [i for i, n in ids.items() if n > 1])
fronts = collections.Counter(c["front"] for c in cards)
print("duplicate fronts", [f[:60] for f, n in fronts.items() if n > 1])
backs = collections.Counter(c["back"] for c in cards)
print("duplicate backs", [b[:60] for b, n in backs.items() if n > 1])
banned = re.compile(r"roughly|about |historically|typically|\.\.\.|…|\bround\b|verifier|builder|unit report|REQUEST", re.I)
print("banned/process hits", [(c["id"], m.group(0)) for c in cards for m in [banned.search(c["front"] + " " + c["back"])] if m])
c84 = next(c for c in cards if c["id"] == "CF1-c084")
print("c084 lesson", c84["lesson"], "grade", c84["grade"], "basis", c84["basis"], "cite", c84["cite"])
l06 = (root / "L06.html").read_text()
for tok in re.findall(r"\d+(?:\.\d+)?", c84["back"]):
    print("c084 number", tok, "in L06:", tok in l06)
print("c084 phrases in L06:", [p in l06 for p in ["tail probability in E1 and the band in E2", "the cents error and the count of standard errors in E1 are not"]])
