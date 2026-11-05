"""Round-10 PC3 slice a: list every TeX macro and every single-letter symbol inside math delimiters of the slice pages."""
import collections
import html
import re
import sys

pages = sys.argv[1:]
macros = collections.Counter()
letters = collections.defaultdict(collections.Counter)
for path in pages:
    with open(path, encoding="utf-8") as fh:
        text = html.unescape(fh.read())
    segments = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, flags=re.S)
    for a, b in segments:
        seg = a or b
        for m in re.findall(r"\\[A-Za-z]+", seg):
            macros[m] += 1
        stripped = re.sub(r"\\[A-Za-z]+", " ", seg)
        for m in re.findall(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", stripped):
            letters[m][path.split('/')[-1]] += 1
        for m in re.findall(r"\\(?:mathbb|mathcal|mathbf|operatorname)\{[^}]*\}", seg):
            macros[m] += 1
print("MACROS", sorted(macros.items()))
print("LETTERS", {k: dict(v) for k, v in sorted(letters.items())})
