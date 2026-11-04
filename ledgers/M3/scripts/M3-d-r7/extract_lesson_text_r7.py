"""Round-7 verifier (slice d): writes plain text of every M3 lesson page to ledgers/M3/scripts/M3-d-r7/out/text/ (tags
stripped, entities unescaped, script and style removed). Used by card_refs_r7.py and read by hand for L08 and L09."""

import html
import re
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "ledgers/M3/scripts/M3-d-r7/out/text"
OUT.mkdir(parents=True, exist_ok=True)
for i in range(1, 10):
    raw = (ROOT / f"course/modules/M/M3/L0{i}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<br\s*/?>|</p>|</li>|</div>|</tr>|</pre>", "\n", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    text = "\n".join(re.sub(r"[ \t]+", " ", line).strip() for line in html.unescape(raw).split("\n"))
    text = re.sub(r"\n\s*\n+", "\n", text)
    (OUT / f"L0{i}.txt").write_text(text, encoding="utf-8")
    print("wrote", f"L0{i}.txt", len(text), "chars")
