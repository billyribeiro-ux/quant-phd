"""Report ellipsis characters in E4 slice-a prose, outside pre/script blocks and KaTeX math (read-only)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
for name in ["index.html", "L01.html", "L02.html", "L03.html"]:
    text = (ROOT / "course/modules/E/E4" / name).read_text(encoding="utf-8")
    text = re.sub(r"<pre.*?</pre>", "", text, flags=re.S)
    text = re.sub(r"<script.*?</script>", "", text, flags=re.S)
    text = re.sub(r"\\\[.*?\\\]", "", text, flags=re.S)
    text = re.sub(r"\\\(.*?\\\)", "", text, flags=re.S)
    hits = [m.start() for m in re.finditer(r"\.\.\.|…", text)]
    print(name, "ellipsis hits outside code and math:", len(hits))
