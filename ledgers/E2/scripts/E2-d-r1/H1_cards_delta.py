# H1 (closing delta, pin d9de2fe5 vs base pin 2a805c83): card-level checks for course/modules/E/E2/cards.json.
# 1. every number in a card's front/back appears in its lesson HTML text (commas removed)
# 2. duplicate ids and fronts, grade set, basis on C cards
# 3. ids and cards that differ from the base pin 2a805c83 and from 95f3f8cb
import json, re, subprocess, sys, html
from pathlib import Path
root = Path(sys.argv[1])
def git_cards(rev):
    return json.loads(subprocess.run(["git", "-C", str(root), "show", rev + ":course/modules/E/E2/cards.json"],
                                     capture_output=True, text=True, check=True).stdout)
cards = json.loads((root / "course/modules/E/E2/cards.json").read_text(encoding="utf-8"))
base = {c["id"]: c for c in git_cards("2a805c83")}
old = {c["id"]: c for c in git_cards("95f3f8cb")}
cur = {c["id"]: c for c in cards}
def lesson_text(lid):
    raw = (root / ("course/modules/E/E2/" + lid + ".html")).read_text(encoding="utf-8")
    raw = re.sub(r"</?[a-zA-Z][^>]*>", " ", raw)
    return html.unescape(raw)
texts = {}
num_re = re.compile(r"\d[\d,]*(?:\.\d+)?")
problems = []
fronts = {}
ids = {}
for c in cards:
    lid = c["lesson"]
    if lid not in texts:
        texts[lid] = lesson_text(lid)
        texts[lid + "_nc"] = texts[lid].replace(",", "")
    s = c["front"] + " " + c["back"]
    for n in sorted(set(num_re.findall(s))):
        n2 = n.rstrip(",")
        if not n2:
            continue
        if n2 in texts[lid] or n2.replace(",", "") in texts[lid + "_nc"]:
            continue
        problems.append(c["id"] + " (" + lid + "): number " + repr(n2) + " not found in lesson text")
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
    ids[c["id"]] = ids.get(c["id"], 0) + 1
print("cards:", len(cards))
print("grade values:", sorted(set(str(c.get("grade")) for c in cards)))
print("duplicate ids:", {k: v for k, v in ids.items() if v > 1})
print("number problems:", len(problems))
for p in problems:
    print("  ", p)
print("duplicate fronts:", {k: v for k, v in fronts.items() if len(v) > 1})
print("ids removed vs base 2a805c83:", sorted(set(base) - set(cur)))
print("ids added vs base 2a805c83:", sorted(set(cur) - set(base)))
print("changed vs base 2a805c83:", sorted(i for i in cur if i in base and base[i] != cur[i]))
print("changed vs 95f3f8cb:", sorted(i for i in cur if i in old and old[i] != cur[i]))
print("C-grade without basis:", [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")])
