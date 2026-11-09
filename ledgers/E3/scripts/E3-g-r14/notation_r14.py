"""Round-14: registered notation symbols and macros against L05-L08 cards and lesson text.
Run as: python -I ledgers/E3/scripts/E3-g-r14/notation_r14.py (from the checkout root)."""
import json
import re

cards = [c for c in json.load(open("course/modules/E/E3/cards.json")) if c["lesson"] in ("L05", "L06", "L07", "L08")]
pat = re.compile(r"(?<![A-Za-z])T(?![A-Za-z])|Phi|gamma_3|gamma_4|R\^\*|R_f|R\^\{e|\\mathbb\{Q\}|\bQ\b")
hits = [(c["id"], m.group(0)) for c in cards for m in pat.finditer(c["front"] + " " + c["back"])]
print("registered-symbol tokens in L05-L08 cards:", hits)
probs = [(c["id"], m.start()) for c in cards for m in re.finditer(r"P\(", c["front"] + " " + c["back"])]
print("P( in cards (probability operator or prior label; registry has \\Prob and no P):", sorted({i for i, _ in probs}))
print("macros in notation.json include \\Prob and \\E:", "\\Prob" in json.load(open("notation/notation.json"))["macros"], "\\E" in json.load(open("notation/notation.json"))["macros"])
