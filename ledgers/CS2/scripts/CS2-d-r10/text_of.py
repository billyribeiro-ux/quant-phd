"""Plain text of a CS2 page: tags stripped, entities unescaped, one block per line. Usage: text_of.py <page.html>"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8")
src = re.sub(r"<(script|style)\b.*?</\1>", " ", src, flags=re.S)
src = re.sub(r"</(p|li|h[1-6]|pre|tr|div|section|dd|dt|figcaption)>|<br\s*/?>", "\n", src)
src = re.sub(r"<[^>]+>", " ", src)
for line in html.unescape(src).splitlines():
    line = re.sub(r"[ \t]+", " ", line).strip()
    if line:
        print(line)
