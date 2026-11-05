"""Round 8, slice e: scan card faces for the registered notation symbols in their unicode and TeX-like spellings.

Registered (notation/notation.json): T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, blackboard Q. Also the transpose glyph in use.
Usage: python -I card_glyph_scan.py <cards.json>
"""
import json
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
pats = {
    "Phi": r"Φ|\\Phi|Phi",
    "gamma": r"γ|\\gamma|gamma",
    "R_f": r"R_f|R_\{f\}",
    "R^*": r"R\^\*|R\^\\ast|R\*",
    "R^{e*}": r"R\^\{e",
    "blackboard Q": r"ℚ|\\mathbb\{Q\}|\bQ\b",
    "plain T as a superscript or variable": r"\^T\b|\^\{T\}|(?<![A-Za-z])T(?![A-Za-z])",
    "transpose glyph U+22A4": r"⊤",
}
for name, p in pats.items():
    hits = [(c["id"], m.group(0)) for c in cards for m in re.finditer(p, c["front"] + " " + c["back"])]
    print(name, len(hits), hits[:8])
