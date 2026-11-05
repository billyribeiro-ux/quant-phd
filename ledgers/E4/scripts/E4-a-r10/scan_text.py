"""Scan E4 slice-a pages for macros, notation hits, banned phrases, process words and scope words.

Usage: .venv/bin/python -I ledgers/E4/scripts/E4-a-r10/scan_text.py
Prints every hit with its file and a 60-character context. Read-only.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ["course/modules/E/E4/index.html", "course/modules/E/E4/L01.html", "course/modules/E/E4/L02.html",
         "course/modules/E/E4/L03.html"]
PATTERNS = {
    "macros": r"\\[A-Za-z]+",
    "raw-mathbb": r"\\mathbb\{[A-Za-z]\}",
    "registered-symbol-risk": r"\\Phi|\\gamma|R\^\\ast|R_f|R\^\{e|\\pi_\{?[a-z]\}?\\,?T",
    "banned": r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly",
    "process-words": r"\bround \d|\bverifier|\bbuilder|\bunit report|\bREQUEST",
    "state-price": r"state price",
    "scope": r"\b(every|all|always|never|only|any|same|exactly)\b",
}
for rel in PAGES:
    text = (ROOT / rel).read_text(encoding="utf-8")
    body = re.sub(r"<script.*?</script>", "", text, flags=re.S)
    for name, pat in PATTERNS.items():
        hits = list(re.finditer(pat, body if name != "macros" else body, flags=re.I if name in {"banned", "process-words", "state-price"} else 0))
        if name == "macros":
            found = sorted({h.group(0) for h in hits})
            print(f"{rel} macros: {found}")
            continue
        for h in hits:
            ctx = body[max(0, h.start() - 60): h.end() + 40].replace("\n", " ")
            print(f"{rel} [{name}] {h.group(0)!r}: ...{ctx}...")
