# Lists every card of lessons L22, L23, L24 in cards.json (id, grade, basis, front, back). Usage: python -I <script> <root>
import json, os, sys
root = os.path.abspath(sys.argv[1])
cards = json.load(open(os.path.join(root, "course/modules/M/M2/cards.json"), encoding="utf-8"))
from collections import Counter
print("counts by lesson", dict(Counter(c["lesson"] for c in cards if c["lesson"] in ("L22", "L23", "L24"))))
for c in cards:
    if c["lesson"] in ("L22", "L23", "L24"):
        print(c["id"], c["lesson"], "grade=" + str(c.get("grade", "-")), "basis=" + str(c.get("basis", "-")))
        print("  F:", c["front"])
        print("  B:", c["back"])
