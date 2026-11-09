"""List every TeX macro and every single-letter or registered symbol used inside math on the slice pages."""
import html
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
pages = ["index", "L01", "L02", "L03", "L04"]
macros: Counter[str] = Counter()
letters: dict[str, Counter[str]] = {}
for p in pages:
    text = html.unescape((root / f"course/modules/M/M5/{p}.html").read_text(encoding="utf-8"))
    segs = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S)
    for a, b in segs:
        s = a or b
        for m in re.findall(r"\\[A-Za-z]+", s):
            macros[m] += 1
        s2 = re.sub(r"\\[A-Za-z]+", " ", s)
        for ch in re.findall(r"(?<![A-Za-z])[A-Za-z](?![A-Za-z])", s2):
            letters.setdefault(ch, Counter())[p] += 1
print("MACROS:", sorted(macros.items(), key=lambda kv: -kv[1]))
print("SINGLE LETTERS (symbol: pages):")
for ch in sorted(letters):
    print(" ", ch, dict(letters[ch]))
