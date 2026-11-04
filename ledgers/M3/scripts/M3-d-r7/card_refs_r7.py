"""Round-7 verifier (slice d): every card's numbered references and numbers must occur in the lesson it names.

Lesson text is extracted from course/modules/M/M3/L0n.html (tags stripped, entities unescaped, the expected blocks
included). For each card: (a) every 'Kind N.M' reference in the card (Definition, Theorem, Proposition, Lemma, Remark,
Corollary, Example, Problem, Fact, Section) must occur in the lesson text, or in the card's own text when the card names
another lesson; (b) every number of two or more digits in the back must occur in the lesson text or in the card.
Usage: .venv/bin/python -I ledgers/M3/scripts/M3-d-r7/card_refs_r7.py
"""

import html
import json
import re
from pathlib import Path

ROOT = Path.cwd()
MOD = ROOT / "course/modules/M/M3"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))


def lesson_text(name: str) -> str:
    raw = (MOD / f"{name}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))


texts = {f"L0{i}": lesson_text(f"L0{i}") for i in range(1, 10)}
REF = re.compile(r"\b(Definition|Theorem|Proposition|Lemma|Remark|Corollary|Example|Problem|Fact|Section)\s+(\d+(?:\.\d+)?[a-z]?(?:\([a-z]\))?)")
NUM = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w])")
misses: list[str] = []
refs_checked = 0
nums_checked = 0
for card in cards:
    lt = texts[card["lesson"]]
    own = card["front"] + " " + card["back"]
    for kind, num in set(REF.findall(card["back"] + " " + card["front"])):
        refs_checked += 1
        pat = f"{kind} {num}"
        if pat not in lt and pat not in own.replace("  ", " "):
            misses.append(f"{card['id']} {card['lesson']}: '{pat}' not in lesson text")
    for num in sorted(set(NUM.findall(card["back"]))):
        core = num.lstrip("-")
        if len(core.replace(".", "")) < 2:
            continue
        nums_checked += 1
        if re.search(r"(?<![\w.])" + re.escape(core) + r"(?![\w])", lt) or core in own:
            continue
        if "." in core and re.search(r"(?<![\w.])" + re.escape(core.rstrip("0").rstrip(".")), lt):
            continue
        misses.append(f"{card['id']} {card['lesson']}: number '{num}' not in lesson text or card")
print("references checked:", refs_checked)
print("numbers checked:", nums_checked)
for m in sorted(misses):
    print("MISS", m)
print("misses:", len(misses))
