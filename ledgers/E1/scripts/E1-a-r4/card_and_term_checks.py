"""Round-4 checks for E1 slice a: card symbols and terms against the current lesson text."""
import json
import re
from pathlib import Path

root = Path("/tmp/verifyB4-E1-a/course/modules/E/E1")
pages = {p: (root / f"{p}.html").read_text(encoding="utf-8") for p in ("L01", "L02", "L03")}
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))

for c in cards:
    if c["lesson"] not in pages:
        continue
    text = c["front"] + " " + c["back"]
    page = pages[c["lesson"]]
    if re.search(r"\bx\*|\by\*", text):
        print(c["id"], "uses x* or y*; lesson contains x* or y*:", bool(re.search(r"x\^\\\*|y\^\\\*|x\*|y\*", page)))
    if re.search(r"\bonly\b", text):
        print(c["id"], "scope word 'only' in card:", text[text.find("only") - 40 : text.find("only") + 20])
    for term in ("indifference",):
        if term in text.lower():
            print(c["id"], f"term {term!r} in card; occurrences in its lesson:", page.lower().count(term))

l01 = pages["L01"]
print("L01 'x_bar' occurrences:", l01.count("\\bar{x}"), "; 'only at the optimum' in L01:", "only at the optimum" in pages["L03"] or "only at the optimum" in l01)
print("L01 Prop 2.3 misconception wording:", re.findall(r"Proposition 2\.3 gives the equality[^<]{0,30}", l01))
