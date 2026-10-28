"""Round-3 check: slice cards whose lesson result now sits under Assumption 1 (derivative of exp or sin).

Run: python3 -I card_hypothesis_scan.py <checkout>
For each listed card, prints grade and whether its back text names the assumption. The list is the set of
cards found by reading the Assumption-1 passages of L13-L18 (the lesson sentence is in the adjacent comment).
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/M/M2"
cards = {c["id"]: c for c in json.loads((root / "cards.json").read_text(encoding="utf-8"))}
# id -> lesson passage that carries Assumption 1 (checked by reading the page, round 3)
listed = {
    "M2-c188": "L13 Example 2.3 (Under Assumption 1; key row T)",
    "M2-c189": "L13 Example 2.3 (key row T)",
    "M2-c190": "L13 Example 2.3 ratio (key row T, under Assumption 1)",
    "M2-c206": "L14 Example 4.1 (Under Assumption 1)",
    "M2-c211": "L14 Proposition 5.2 (Assume Assumption 1)",
    "M2-c241": "L16 Example 1.3 (Under Assumption 1)",
    "M2-c252": "L17 Example 1.2 (Under Assumption 1)",
    "M2-c255": "L17 Example 2.3 (Under Assumption 1)",
    "M2-c258": "L17 Problem R1 (Under Assumption 1)",
    "M2-c262": "L17 Example 2.3 formula (Under Assumption 1)",
    "M2-c264": "L17 Problem R1 key row (Under Assumption 1)",
    "M2-c277": "L18 Problem R1 (Under Assumption 1)",
}
for cid, where in listed.items():
    c = cards[cid]
    named = "Assumption 1" in c["back"] or "assum" in c["back"].lower()
    print(f"{cid} {c['lesson']} grade={c.get('grade')} names_assumption={named} lesson={where}")
print("M2-c188 grade C vs key-results row T:", cards["M2-c188"].get("grade"), "vs T")
