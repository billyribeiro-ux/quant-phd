# Verifier script (M7-b round 1): L04-L06 cards: C-graded cards carry a basis naming the lab, SIMULATED where a lab input is used;
# T-graded cards carry no basis; cards that mention "Lab 1" are C-graded.
import json

cards = [c for c in json.load(open("course/modules/M/M7/cards.json", encoding="utf-8")) if c["lesson"] in ("L04", "L05", "L06")]
problems = []
for c in cards:
    basis = c.get("basis", "")
    text = c["front"] + " " + c["back"]
    if c["grade"] == "C" and not basis.startswith("Lab"):
        problems.append((c["id"], "C without lab basis"))
    if c["grade"] == "C" and "SIMULATED" not in basis:
        problems.append((c["id"], "C basis without SIMULATED"))
    if c["grade"] == "T" and basis:
        problems.append((c["id"], "T with basis"))
    if "Lab 1" in text and c["grade"] != "C":
        problems.append((c["id"], "mentions Lab 1 but not C"))
print("L04-L06 cards", len(cards), "C", sum(c["grade"] == "C" for c in cards), "T", sum(c["grade"] == "T" for c in cards))
print("problems", problems)
