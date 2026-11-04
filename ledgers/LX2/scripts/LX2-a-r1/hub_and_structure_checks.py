"""Hub, placement arithmetic, title, registry and concept-anchor checks for LX2 slice a.

Usage: python3 -I hub_and_structure_checks.py <repo_root>
Reads the repository only. Prints one line per check with the value observed.
"""

import json
import re
import sys
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])
hub = (root / "course/modules/LX/LX2/index.html").read_text(encoding="utf-8")
l01 = (root / "course/modules/LX/LX2/L01.html").read_text(encoding="utf-8")
l02 = (root / "course/modules/LX/LX2/L02.html").read_text(encoding="utf-8")
concepts = (root / "course/concepts.html").read_text(encoding="utf-8")

print("hub data-hours-lessons / data-hours-project:",
      re.search(r'data-hours-lessons="(\d+)"', hub).group(1), re.search(r'data-hours-project="(\d+)"', hub).group(1))
print("lesson hours (L01, L02):", re.search(r'data-hours="(\d+)"', l01).group(1), re.search(r'data-hours="(\d+)"', l02).group(1))
print("lessons 4*9 + project 14 =", 4 * 9 + 14, "; project share 14/50 =", Fraction(14, 50), "=", str(Fraction(14, 50) * 100) + "%")
print("placement: 8/10 =", Fraction(8, 10), "; 7/10 =", Fraction(7, 10), "; mastery bar", re.search(r'data-mastery="([\d.]+)"', hub).group(1))
print("item 3: 100/1.1 =", round(100 / 1.1, 6), "-> 2 dp", f"{100 / 1.1:.2f}")
print("item 9: 100.10 - 99.50 =", f"{Fraction('100.10') - Fraction('99.50')}")
print("item 10: 6/8 =", Fraction(6, 8), "=", float(Fraction(6, 8)))
bias = [Fraction(10) - 11, Fraction(12) - 13, Fraction(9) - 8]
print("item 11 differences:", [str(b) for b in bias], "sum", str(sum(bias)), "mean", str(sum(bias) / 3), "=", f"{float(sum(bias) / 3):.4f}")
print("item 12 derivative of x^2 at 3:", 2 * 3, "; d/dx x^2 y at (2,3):", 2 * 2 * 3)
print("quantifier negation item: negation of 'for every x in S, P(x) holds' is 'there exists x in S with P(x) fails'")

fc1_title_hub = re.search(r'<a href="\.\./\.\./FC/FC1/index\.html">([^<]+)</a>', hub)
print("hub FC1 link text:", fc1_title_hub.group(1) if fc1_title_hub else None)
fc1_html = (root / "course/modules/FC/FC1/index.html").read_text(encoding="utf-8")
print("FC1 index <h1>:", re.search(r"<h1>([^<]+)</h1>", fc1_html).group(1))
cur = (root / "curriculum/02-economics-finance-core.yaml").read_text(encoding="utf-8")
print("curriculum FC1 title line:", re.search(r'id: FC1\n\s+title: "([^"]+)"', cur).group(1))
m05 = (root / "curriculum/05-macro-alternatives.yaml").read_text(encoding="utf-8")
print("curriculum SR4 title and prereqs:", re.search(r'id: SR4\n\s+title: "([^"]+)"', m05).group(1),
      re.search(r"id: SR4\n[\s\S]*?prereqs: \[([^\]]+)\]", m05).group(1))

ref = json.loads((root / "references/references.json").read_text(encoding="utf-8"))
blob = json.dumps(ref).lower()
for term in ["dodd", "mifid", "fiduciary", "texas gulf", "sulphur", "esma", "eur-lex", "europa"]:
    print(f"registry contains '{term}':", term in blob)
keys = {e["key"] for e in ref["entries"]}
for k in ["gpondsecurities", "gpondsecuritiesb", "gpo1983dirks", "gpo1997united", "cfandcode", "frb2026fed"]:
    print("registry key", k, "present:", k in keys)

for cid in ["exchange-vs-otc", "limit-order-book", "order-types", "bid-ask-spread", "quantifiers", "present-value",
            "derivative", "partial-derivative", "comparative-statics", "evidence-grade", "project-ladder",
            "securities-registration", "exchange-act-1934"]:
    print("concepts.html anchor", cid, "count:", len(re.findall(rf'id="{cid}"', concepts)))
print("P0.1 entries read 'not yet released':", len(re.findall(r'id="(evidence-grade|project-ladder)">.*?not yet released', concepts)))
print("hub lesson titles:", re.findall(r'<span class="card-title">([^<]+)</span>', hub)[:2])
print("L01 h1:", re.search(r"<h1>([^<]+)</h1>", l01).group(1))
print("L02 h1:", re.search(r"<h1>([^<]+)</h1>", l02).group(1))
print("Texas Gulf / Chiarella / Cady mentions in slice pages:",
      len(re.findall(r"Texas Gulf|Chiarella|Cady", hub + l01 + l02)))
