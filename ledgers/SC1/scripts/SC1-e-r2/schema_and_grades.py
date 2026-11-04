"""Schema, grade/basis pairing, cite emptiness, markup and lab-basis audit of SC1 cards (read-only, stdlib).
Usage: schema_and_grades.py <cards.json>
"""
import json
import re
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
print("cards:", len(cards), "distinct ids:", len({c["id"] for c in cards}))
print("keys:", sorted({k for c in cards for k in c}))
print("cites nonempty:", [c["id"] for c in cards if c["cite"]])
print("grade without basis:", [c["id"] for c in cards if "grade" in c and not c.get("basis")])
print("basis without grade:", [c["id"] for c in cards if "basis" in c and "grade" not in c])
print("graded:", sum(1 for c in cards if "grade" in c), "of", len(cards), Counter(c.get("grade") for c in cards))
print("per lesson:", sorted(Counter(c["lesson"] for c in cards).items()))
print("T cards whose basis names a lab:", [c["id"] for c in cards if c.get("grade") == "T" and re.search(r"[Ll]ab|SIMULATED", c.get("basis", ""))])
print("C cards whose basis names no lab:", [c["id"] for c in cards if c.get("grade") == "C" and not re.search(r"[Ll]ab", c.get("basis", ""))])
markup = re.compile(r"</?(a|p|em|span|sup|sub|code|br|div|strong|dfn|li|ul)[ >/]")
print("cards with HTML markup:", [c["id"] for c in cards if markup.search(c["front"] + c["back"])])
