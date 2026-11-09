"""Closing-delta check of the frb2026fed claim spans on project.html against the fetched sources.

For every span with data-cite="frb2026fed", the span text is searched (whitespace and quote-normalised) in the
plain text of the HTML page (tags stripped, entities unescaped) and in the combined PDF text (SR2602.pdf).
Usage: python3 -I closing_quote_check.py <checkout> <html_src> <combined_pdf_text>
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

checkout, htm_path, pdf_txt_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])


def norm(s: str) -> str:
    s = html.unescape(s)
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = s.replace("—", "-").replace("–", "-").replace(" ", " ")
    s = re.sub(r"<[^>]+>", " ", s) if "<" in s else s
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


page = (checkout / "course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
htm = norm(re.sub(r"<script.*?</script>|<style.*?</style>", " ", htm_path.read_text(encoding="utf-8", errors="replace"), flags=re.S | re.I))
pdf = norm(pdf_txt_path.read_text(encoding="utf-8", errors="replace").replace("-\n", "").replace("\f", " "))
spans = re.findall(r'<span class="claim"[^>]*data-cite="frb2026fed"[^>]*>(.*?)</span>', page, re.S)
print(f"frb2026fed claim spans: {len(spans)}")
for s in spans:
    t = norm(re.sub(r"<[^>]+>", " ", s)).strip('"').strip()
    in_htm = t in htm
    in_pdf = t in pdf
    print(f"htm={'Y' if in_htm else 'N'} pdf={'Y' if in_pdf else 'N'} | {t[:110]}")
