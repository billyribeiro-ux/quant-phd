"""Slice e (round 2): card symbols against the registered notation (notation/notation.json).

Usage (from the checkout root): python -I ledgers/E4/scripts/E4-e-r2/notation_check.py
Reports every card occurrence of a registered symbol's letter as a standalone math symbol, and any Greek gamma.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CARDS = Path("course/modules/E/E4/cards.json")
NOTATION = Path("notation/notation.json")


def main() -> None:
    notation = json.loads(NOTATION.read_text(encoding="utf-8"))
    registered = [s["symbol"] for s in notation["symbols"]]
    print("registered symbols:", registered)
    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    standalone_t = re.compile(r"(?<![A-Za-z^])T(?![A-Za-z])")
    transpose = re.compile(r"\^T\b")
    hits: list[str] = []
    for card in cards:
        for field in ("front", "back"):
            text = card[field]
            for match in standalone_t.finditer(text):
                context = text[max(0, match.start() - 3) : match.end() + 3]
                hits.append(f"{card['id']} {field}: {context!r}")
    print("standalone T in card text:", len(hits))
    for hit in hits:
        print("  ", hit)
    print("superscript transposes ^T in cards:", sum(len(transpose.findall(c["front"] + c["back"])) for c in cards))
    greek_gamma = [c["id"] for c in cards if "γ" in c["front"] + c["back"]]
    print("Greek gamma in cards:", greek_gamma)
    checks = {
        "Phi": r"Φ",
        "gamma_3": r"γ_3",
        "gamma_4": r"γ_4",
        "R^* (asterisk)": r"R\^\*|R\*",
        "R^{e*}": r"R\^e\*",
        "R_f": r"R_f",
        "Q (blackboard)": r"ℚ|\\mathbb\{Q\}",
    }
    for label, pattern in checks.items():
        found = [c["id"] for c in cards if re.search(pattern, c["front"] + c["back"])]
        print(f"registered symbol {label} in cards:", found)


if __name__ == "__main__":
    main()
