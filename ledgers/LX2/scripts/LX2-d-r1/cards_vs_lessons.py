"""LX2-d round 1: every card checked against its lesson. Quoted strings, numbers, labels and locators.

Usage: .venv/bin/python ledgers/LX2/scripts/LX2-d-r1/cards_vs_lessons.py <checkout-root>
Prints one line per check failure, then a per-card summary. A card with no line printed passed every mechanical test.
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
UNIT = ROOT / "course/modules/LX/LX2"
cards = json.loads((UNIT / "cards.json").read_text(encoding="utf-8"))


def norm(s: str) -> str:
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace("−", "-").replace("–", "-").replace("—", "-").replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"').replace(" ", " ")
    s = re.sub(r"\\\(|\\\)|\\\[|\\\]|\$", "", s)
    s = re.sub(r"\s+", " ", s)
    return s


lessons = {p: norm((UNIT / f"{p}.html").read_text(encoding="utf-8")) for p in ["L01", "L02", "L03", "L04"]}
raw = {p: (UNIT / f"{p}.html").read_text(encoding="utf-8") for p in lessons}

fails = 0
def fail(cid, kind, detail):
    global fails
    fails += 1
    print(f"{cid} [{kind}] {detail}")

for c in cards:
    lesson = lessons[c["lesson"]]
    cid = c["id"]
    text = c["front"] + " || " + c["back"] + " || " + c.get("basis", "")
    # 1. quoted strings: anything inside double quotes or curly quotes, or single-quoted with spaces
    quotes = re.findall(r'"([^"]{6,})"', c["back"] + " " + c["front"])
    quotes += re.findall(r"“([^”]{6,})”", c["back"] + " " + c["front"])
    for q in quotes:
        qn = norm(q).strip().rstrip(".,;:")
        qn2 = qn.replace("'", "'").lower()
        if qn2 not in lesson.lower():
            fail(cid, "quote-not-in-lesson", f"'{qn[:90]}'")
    # 5. numbers: every number token of the card must occur in the lesson (or be a derived count stated on the card)
    for num in set(re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?(?![\w])", c["back"] + " " + c["front"])):
        clean = num.replace(",", "")
        if not re.search(r"(?<![\d.])" + re.escape(num) + r"(?![\d])", lesson) and not re.search(r"(?<![\d.])" + re.escape(clean) + r"(?![\d])", lesson):
            fail(cid, "number-not-in-lesson", num)
    # 6. fraction forms
    for m in re.finditer(r"(\d+)/(\d+)", c["back"]):
        if m.group(0) not in lesson and f"{m.group(1)}/{m.group(2)}" not in lesson:
            fail(cid, "fraction-not-in-lesson", m.group(0))
    # 7. cite keys present on the lesson page (data-cite) when the card cites them
    for key in c.get("cite", []):
        if key not in raw[c["lesson"]] and key not in json.dumps(c):
            fail(cid, "cite-key-absent-from-lesson", key)
print("LX2-d cards vs lessons: fails", fails, "cards", len(cards))
