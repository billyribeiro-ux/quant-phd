import json, sys, collections
from pathlib import Path
root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M4/cards.json").read_text())
cnt = collections.Counter(c["lesson"] for c in cards)
print("per-lesson", {k: cnt[k] for k in sorted(cnt)})
ids = [c["id"] for c in cards]
print("duplicate ids", [i for i in set(ids) if ids.count(i) > 1])
for L in ("L05", "L06", "L07"):
    page = (root / f"course/modules/M/M4/{L}.html").read_text()
    for c in cards:
        if c["lesson"] != L:
            continue
        assert c["grade"] in ("T", "C", "X"), c["id"]
        print(L, c["id"], c["grade"], "basis" in c, "back-numbers:", sorted(set(__import__("re").findall(r"\d+/\d+|\d+\.\d+|\b\d+\b", c["back"])))[:6])
