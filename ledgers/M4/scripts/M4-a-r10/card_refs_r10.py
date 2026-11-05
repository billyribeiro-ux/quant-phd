# Round 10: for each L01-L04 card, check (a) every "Proposition/Definition/Example/Remark/Problem/Section/Lesson" reference
# in front/back names a number that exists on the cited lesson page (or the same page), (b) every numeric token of the
# back appears in the lesson HTML (after unescaping and removing LaTeX braces/backslashes).
import html, json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M4/cards.json").read_text(encoding="utf-8"))
pages = {}
for n in ("L01", "L02", "L03", "L04"):
    raw = (root / f"course/modules/M/M4/{n}.html").read_text(encoding="utf-8")
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    pages[n] = (raw, txt)
problems = 0
for c in cards:
    if c["lesson"] not in pages:
        continue
    raw, txt = pages[c["lesson"]]
    body = c["front"] + " " + c["back"]
    # defined labels on the page
    labels = set(re.findall(r"(Proposition|Definition|Example|Remark|Problem|Assumption) (\d+(?:\.\d+)?|[PRME]\d)", txt))
    for kind, num in re.findall(r"(Proposition|Definition|Example|Remark|Problem) (\d+\.\d+|[PRME]\d)", body):
        ok = (kind, num) in labels or re.search(rf"{kind} {re.escape(num)}\b", txt) is not None
        if not ok:
            problems += 1
            print("MISSING-LABEL", c["id"], c["lesson"], kind, num)
    for sec in re.findall(r"Section (\d)", body):
        if not re.search(rf"\b{sec}\b", txt):
            print("SECTION?", c["id"], sec)
    for tok in re.findall(r"\d+/\d+|\d+\.\d+|\b\d+\b", c["back"]):
        if tok in ("1", "0", "2"):
            continue
        t2 = tok
        if t2 not in raw and t2 not in txt:
            problems += 1
            print("NUM-NOT-ON-PAGE", c["id"], c["lesson"], tok, "|", c["back"][:120])
print("card reference problems:", problems, "cards checked:", sum(1 for c in cards if c['lesson'] in pages))
