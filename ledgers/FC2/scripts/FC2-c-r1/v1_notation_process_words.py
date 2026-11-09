"""Round 1 verifier checks for slice c (L07-L08): notation symbols, registered macros, process words, R_f use.

Standard library only. Run from the checkout root:
    .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r1/v1_notation_process_words.py
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = [ROOT / "course" / "modules" / "FC" / "FC2" / "L07.html", ROOT / "course" / "modules" / "FC" / "FC2" / "L08.html"]
PROCESS = re.compile(
    r"\b(verifier|verification|builder|orchestrat\w*|ledger|fragment|round|fixer|TODO|TBD|lorem|placeholder|draft)\b",
    re.I,
)


def math_segments(raw: str) -> list[str]:
    segs = re.findall(r"\\\((.*?)\\\)", raw, flags=re.S)
    segs += re.findall(r"\\\[(.*?)\\\]", raw, flags=re.S)
    return [html.unescape(s) for s in segs]


def main() -> None:
    notation = json.loads((ROOT / "notation" / "notation.json").read_text(encoding="utf-8"))
    registered = {m for m in notation["macros"]}
    print("registered macros:", sorted(registered))
    for page in PAGES:
        raw = page.read_text(encoding="utf-8")
        segs = math_segments(raw)
        standalone_T = [s for s in segs if re.search(r"(?<![A-Za-z\\])T(?![A-Za-z])", s)]
        print(f"{page.name}: math segments={len(segs)} standalone-T segments={standalone_T}")
        rf = [s for s in segs if "R_f" in s or "R_{f}" in s]
        print(f"{page.name}: R_f segments={rf}")
        ast_R = [s for s in segs if re.search(r"R\^\\ast|R\^\*", s)]
        print(f"{page.name}: R^ast segments={ast_R}")
        mathbb = [s for s in segs if "\\mathbb" in s]
        print(f"{page.name}: \\mathbb segments={mathbb}")
        gamma = [s for s in segs if "\\gamma" in s]
        print(f"{page.name}: gamma segments={gamma}")
        text = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
        hits = PROCESS.findall(text)
        print(f"{page.name}: process-word hits={hits}")


if __name__ == "__main__":
    main()
