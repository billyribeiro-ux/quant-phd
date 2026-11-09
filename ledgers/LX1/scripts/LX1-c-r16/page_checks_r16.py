"""Round-15 verifier: page-level scans for project.html (links, key sentence lines, banned words, TeX spans).

Usage: python -I page_checks_r16.py <checkout_root>."""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
src = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
lines = src.split("\n")
ids = set(re.findall(r'\sid="([^"]+)"', src))
hrefs = set(re.findall(r'href="#([^"]+)"', src))
print("in-page hash hrefs:", sorted(hrefs), "missing:", sorted(h for h in hrefs if h not in ids))
print("parity mentions:", src.count("parity"))
print("'lab raises' claim lines:", [i + 1 for i, l in enumerate(lines) if "lab raises" in l or "or the lab raises" in l])
for p in ["11764705.882", "No historical series for your episode", "Round once, at print time", "The analogy holds at step 3",
          "A test would need an interest-rate series", "It is the only lab on this page", "Lab 3 gives 2.47",
          "Official scoring: C1 4", "Official scoring: C1 2", "Proposition 2.2 of that lesson gives",
          "Each printed real value is the nominal debt", "Gold holdings, price levels", "The essay does not divide the printed figures",
          "The lab computes no other start", "Window two holds the changes"]:
    print(f"{p!r}: lines {[i + 1 for i, l in enumerate(lines) if p in l]}")
prose = re.sub(r"<pre.*?</pre>", " ", src, flags=re.S)
prose = re.sub(r"<script.*?</script>", " ", prose, flags=re.S)
text = html.unescape(re.sub(r"<[^>]+>", " ", prose))
text = re.sub(r"\s+", " ", text)
for w in ["build", "builder", "verif", "agent", "REQUESTS", "unit report", "fixer", "Claude", "TODO", "TBD", "lorem",
          "for brevity", "details omitted", "beyond the scope", "it is important to note", "studies show", "experts agree",
          "well known", "obviously", "clearly", "roughly", "historically", "round"]:
    hits = [m.start() for m in re.finditer(re.escape(w), text, flags=re.I)]
    print(f"{w!r}: {len(hits)} hits")
    if w == "round":
        print("   sample:", sorted({text[max(0, h - 12):h + 14] for h in hits})[:8])
spans = re.findall(r"\\\((.*?)\\\)", src)
print("inline TeX spans:", len(spans), "distinct symbols:", sorted({re.sub(r'[^A-Za-z_]', ' ', s).split()[0] for s in spans if re.sub(r'[^A-Za-z_]', ' ', s).split()}))
