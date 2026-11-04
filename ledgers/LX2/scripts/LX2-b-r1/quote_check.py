"""Check every curly-quoted span in L04 (and the L03 quotes, if any) against the source text read by plain curl.

Sources: CFA Standards pages (III(A), VI(A), VI(B)) fetched from cfainstitute.org, and the SR 26-2 letter page and
attachment PDF fetched from federalreserve.gov. Normalises curly quotes, dashes and whitespace before comparing.
Reads the cached copies in /tmp/lx2b-src (fetched with curl on this run).
"""

import html
import re
import sys
from pathlib import Path

page = Path(sys.argv[1]).read_text(encoding="utf-8")
body = page[page.find("<main") : page.find("</main>")]
body = re.sub(r"<details.*?</details>", "", body, flags=re.S)
text = html.unescape(re.sub(r"<[^>]+>", " ", body))


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


sources = {
    "III(A)": Path("/tmp/lx2b-src/standards-of-practice-iii-a.txt").read_text(encoding="utf-8"),
    "VI(A)": Path("/tmp/lx2b-src/standards-of-practice-vi-a.txt").read_text(encoding="utf-8"),
    "VI(B)": Path("/tmp/lx2b-src/standards-of-practice-vi-b.txt").read_text(encoding="utf-8"),
    "CODE": Path("/tmp/lx2b-src/code2024.txt").read_text(encoding="utf-8"),
    "SR": Path("/tmp/lx2b-src/sr2602.txt").read_text(encoding="utf-8")
    + Path("/tmp/lx2b-src/plain.txt").read_text(encoding="utf-8"),
}
allsrc = {k: norm(v) for k, v in sources.items()}
quotes = re.findall(r"“(.+?)”", text)
missing = []
for q in quotes:
    n = norm(q).rstrip(".,;:")
    parts = [p.strip(" .,;:") for p in re.split(r"\.\.\.|…", n) if p.strip(" .,;:")]
    hit = [name for name, s in allsrc.items() if all(p in s for p in parts)]
    status = "FOUND in " + ",".join(hit) if hit else "NOT FOUND"
    if not hit:
        missing.append(q)
    print(f"{status:28} | {q[:110]}")
print("quotes:", len(quotes), "not found:", len(missing))
for m in missing:
    print("MISSING:", m)
