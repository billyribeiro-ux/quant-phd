"""List T-graded cards whose basis or text cites a conditional result (Theorem 1.3, Corollaries 1.3-1.5 and 2.6 of Lesson 7/8,
Theorem 2.5, Remarks 1.4/2.4/2.6, Corollary 2.3, Corollary 1.4 of Lesson 8, Problem R3) and show whether the card
front, back or basis names the assumption (A1-A5, Assumption, assuming, hypotheses). Read-only, stdlib.
Usage: hypothesis_scan.py <cards.json>
"""
import json
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
conditional = re.compile(
    r"Theorem 1\.3|Corollary 1\.[345]|Theorem 2\.5|Corollary 2\.6|Remark 1\.4|Corollary 2\.3|Remark 2\.4|Corollary 1\.4|Problem R3"
)
named = re.compile(r"A[1-5]|Assum|assum|hypoth|Hypoth|under the|Under the|Under H|under H|H1|H2")
for c in cards:
    if c.get("grade") != "T":
        continue
    text = c["front"] + " " + c["back"] + " " + c["basis"]
    if not conditional.search(text):
        continue
    front_back_named = bool(named.search(c["front"] + " " + c["back"]))
    basis_named = bool(named.search(c["basis"]))
    print(f"{c['id']} front/back names assumption={front_back_named} basis names assumption={basis_named} | basis: {c['basis'][:90]}")
