"""Scan project.html visible prose (outside <pre>, <code>, <script>, <style>) for banned phrases, process words,
out-of-closure concept names (plan section 4, D1-D10), forbidden symbols (plan section 2.3) and external resources.
Usage: python -I prose_scan_r6.py <checkout-root>. Prints each hit with its line number; prints counts."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
raw = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
lines = raw.split("\n")
text_lines = []
in_skip = False
for i, line in enumerate(lines, 1):
    stripped = line
    if re.search(r"<(pre|script|style)\b", stripped):
        in_skip = True
    if in_skip:
        if re.search(r"</(pre|script|style)>", stripped):
            in_skip = False
        text_lines.append((i, ""))
        continue
    stripped = re.sub(r"<[^>]+>", " ", stripped)
    text_lines.append((i, html.unescape(stripped)))

patterns = {
    "banned": [r"\bTODO\b", r"\bTBD\b", r"lorem", r"for brevity", r"details omitted", r"beyond the scope",
               r"left as an exercise", r"you can add more", r"it is important to note", r"studies show",
               r"experts agree", r"it is well known", r"\bobviously\b", r"\bclearly\b", r"\.\.\."],
    "process": [r"\bverif", r"\bbuilder", r"\bround \d", r"\bfixture", r"\bruling", r"\barchitect",
                r"\bblind\b", r"\bREQUEST", r"\bfixer\b", r"\bunit report"],
    "out_of_closure": [r"\bBayes", r"state price", r"efficient[- ]markets", r"\bmartingale", r"fixed[- ]point",
                       r"Banach", r"completeness of the reals", r"common knowledge", r"noise-trader risk",
                       r"Walras", r"determinacy", r"two-fund", r"diagnostic expect", r"informed trading"],
    "symbols": [r"\\mathbb", r"\\Phi", r"\\gamma", r"R\^\\ast", r"R\^\{e\\ast\}", r"\\Pr\b"],
    "external": [r"https?://", r"<iframe", r"<img", r"<svg", r"cdn\."],
}
counts: dict[str, int] = {k: 0 for k in patterns}
for group, pats in patterns.items():
    for pat in pats:
        for i, t in text_lines:
            if t and re.search(pat, t, re.I if group in ("banned", "process", "out_of_closure", "external") else 0):
                counts[group] += 1
                print(f"{group} | {pat} | line {i}: {t.strip()[:160]}")
print("counts:", counts)
# math-span scan: every macro used between \( and \) or \[ and \] on the page
spans = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, re.S)
macros = sorted({m for a, b in spans for m in re.findall(r"\\([A-Za-z]+)", a + b)})
print("macros used in math spans:", macros)
