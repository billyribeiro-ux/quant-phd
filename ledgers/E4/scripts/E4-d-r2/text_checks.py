"""Text checks on course/modules/E/E4/project.html (verifier, slice d, round 1).

Usage: python -I ledgers/E4/scripts/E4-d-r2/text_checks.py <repo-root>
1. Sentence count of the spec's Context paragraph (BUILDER_RULES 5.2 requires 2 to 4 sentences).
2. Single-letter symbols used in math spans, and any use of the registered-symbol traps (T, \\Phi, \\gamma, \\mathbb{Q}, R^*).
3. Macros used in math spans.
"""

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")

m = re.search(r"<dt>Context</dt>\s*<dd>(.*?)</dd>", page, flags=re.S)
text = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
text = re.sub(r"\\\(.*?\\\)", "X", text, flags=re.S)
sentences = [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if s]
print("1. Context sentences:", len(sentences))
for s in sentences:
    print("   -", s[:100])

maths = [a or b for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", page, flags=re.S)]
letters: set[str] = set()
for mm in maths:
    letters.update(re.findall(r"(?<![\\A-Za-z])([A-Za-z])(?![A-Za-z])", mm))
print("2. single letters in math spans:", sorted(letters))
traps = [mm[:80] for mm in maths if re.search(r"(?<![\\A-Za-z])T(?![A-Za-z])|\\Phi|\\gamma|\\mathbb|R\^\\ast|R\^\{e", mm)]
print("   trap hits (T, Phi, gamma, mathbb, R^*):", traps)
macros = sorted({c for mm in maths for c in re.findall(r"\\[A-Za-z]+", mm)})
print("3. macros used in math spans:", macros)
