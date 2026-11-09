"""LX1-c round 19: mechanical scans of course/modules/LX/LX1/project.html and the embedded snapshot.

Usage: python -I scan_r19.py <checkout_root>. Prints: TeX symbols used on the page (checked by hand against
notation/notation.json), process-word hits in learner prose, scope-word counts, internal anchor and concept-link
checks, and per-column blank counts of fx_monthly.csv (checked against MANIFEST and the page's Data section).
"""
import csv
import html
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]).resolve()
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
tex = [html.unescape(t) for t in re.findall(r"\\\((.*?)\\\)", page, re.S)]
symbols = sorted({m for t in tex for m in re.findall(r"\\[A-Za-z]+|[A-Za-z](?:_\{?[A-Za-z0-9\-]+\}?)?", t)})
print("TeX symbols on the page:", symbols)
registered = [s["symbol"] for s in __import__("json").loads((root / "notation/notation.json").read_text())["symbols"]]
print("registered program-wide symbols (notation.json):", registered)
print("page symbols that collide with a registered symbol:", sorted(set(symbols) & set(registered)))

prose = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>|<pre.*?</pre>", " ",
                                                      page, flags=re.S)))
for word in ("builder", "verifier", "round", "ruling", "architect", "fixer", "coordinator", "agent", "TODO", "placeholder"):
    hits = re.findall(r"\b" + word + r"\b", prose, re.I)
    print(f"process word {word!r}: {len(hits)}")
for word in ("only", "all", "every", "always", "never", "any", "same", "drives", "exactly", "the first", "the last"):
    print(f"scope word {word!r}: {len(re.findall(r'\b' + word + r'\b', prose, re.I))}")

ids = set(re.findall(r'id="([^"]+)"', page))
bad = [h for h in set(re.findall(r'href="([^"]+)"', page)) if h.startswith("#") and h[1:] not in ids]
print("internal anchors with no target:", bad)
missing = []
for h in set(re.findall(r'href="([^"]+)"', page)):
    f = h.split("#")[0]
    if f and not h.startswith("http") and not (root / "course/modules/LX/LX1" / f).exists():
        missing.append(h)
print("relative hrefs whose file is missing:", missing)

rows = list(csv.DictReader((root / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8")))
for col in [c for c in rows[0] if c != "month"]:
    blanks = [r["month"] for r in rows if r[col] == ""]
    print(f"fx_monthly {col}: rows={len(rows)} blank={len(blanks)}" + (f" blank {blanks[0]}..{blanks[-1]}" if blanks else ""))
