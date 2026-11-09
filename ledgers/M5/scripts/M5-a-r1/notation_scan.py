"""Scan the math segments of the slice pages for registered-symbol conflicts and list every macro used.

Usage: python3 -I ledgers/M5/scripts/M5-a-r1/notation_scan.py <checkout-root>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PAGES = ["index", "L01", "L02", "L03", "L04"]
SYMBOLS = [
    r"\bT\b",
    r"\\Phi",
    r"\\gamma_[34]",
    r"\\ast",
    r"R_f",
    r"\\mathbb\{Q\}",
    r"\\E\b",
    r"\\Prob",
    r"\\Var",
    r"\\se\b",
]
MATH = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
MACRO = re.compile(r"\\([A-Za-z]+)")


def main() -> None:
    root = Path(sys.argv[1])
    registry = json.loads((root / "course" / "assets" / "data" / "notation.json").read_text(encoding="utf-8"))
    print("registered macros:", sorted(registry["macros"]))
    for page in PAGES:
        text = (root / "course" / "modules" / "M" / "M5" / f"{page}.html").read_text(encoding="utf-8")
        math = [a or b for a, b in MATH.findall(text)]
        macros = sorted({m for seg in math for m in MACRO.findall(seg)})
        print(page, "math segments:", len(math), "macros:", macros)
        for pattern in SYMBOLS:
            for seg in math:
                for hit in re.finditer(pattern, seg):
                    print(f"  {page}: {pattern} in ...{seg[max(0, hit.start() - 40) : hit.end() + 40]}...")


if __name__ == "__main__":
    main()
