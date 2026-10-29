"""For each card, every labelled item it cites (Definition/Theorem/Proposition/... with number) must occur in its lesson text
or in another lesson of the unit. Prints unresolved citations."""
import json, re, html
base = "course/modules/CF/CF8/"
cards = json.load(open(base + "cards.json"))
txt = {}
for L in ["L01", "L02", "L03", "L04", "L05"]:
    raw = open(base + L + ".html", encoding="utf-8").read()
    txt[L] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
allt = " ".join(txt.values())
pat = re.compile(r"\b(Definition|Theorem|Proposition|Corollary|Remark|Assumption|Convention|Example|Problem|Misconception|Lab|Section)\s+([0-9A-Z][0-9.]*(?:\([a-z]\))?)")
bad = 0
for c in cards:
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    for kind, num in sorted(set(pat.findall(text))):
        if kind == "Section":
            continue
        probe = f"{kind} {num}"
        if probe.rstrip(".") not in allt and probe.rstrip(".") not in txt[c["lesson"]]:
            bad += 1
            print(c["id"], c["lesson"], "UNRESOLVED:", probe)
print("unresolved", bad)
