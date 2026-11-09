"""Round-6 prose, notation and HTML checks for M5 L08-L10 (delta and carried rows)."""
import html
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
M5 = ROOT / "course/modules/M/M5"
pages = {L: (M5 / f"{L}.html").read_text(encoding="utf-8") for L in ("L08", "L09", "L10")}

class Strict(HTMLParser):
    pass

for L, t in pages.items():
    p = Strict()
    p.feed(t)
    p.close()
    print(f"{L}: html.parser read without error ({len(t)} chars)")
print("L09 \\bstock hits:", len(re.findall(r"\bstock", pages["L09"], re.I)))
t10 = html.unescape(re.sub(r"<[^>]+>", " ", pages["L10"]))
print("L10 0.491631 in page text:", "0.491631" in t10, "| all_within_2_mesh True in page:", "all_within_2_mesh" in t10)
print("kappa/κ occurrences in M5 L08-L10 pages (line numbers):",
      [(L, i + 1) for L, t in pages.items() for i, l in enumerate(t.splitlines()) if "\\kappa" in l or "κ" in l])
notation = (ROOT / "course/assets/data/notation.json").read_text(encoding="utf-8")
print("kappa registered in notation.json:", ("kappa" in notation) or ("κ" in notation))
for L in ("L08", "L09", "L10"):
    print(L, "forms present in page: 10^{-6}", "10^{-6}" in pages[L], "| 10^{-12}", "10^{-12}" in pages[L],
          "| 10^{-2}", "10^{-2}" in pages[L], "| 10^{-4}", "10^{-4}" in pages[L], "| sqrt{3}/2", "\\sqrt{3}/2" in pages[L])
