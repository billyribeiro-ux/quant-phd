"""Plain-text extraction of L01-L09 for the card cross-check (tags stripped, '<' kept)."""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for i in range(1, 10):
    s = (root / f"course/modules/E/E1/L0{i}.html").read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    s = re.sub(r"<(br|/p|/li|/h[1-6]|/div|/tr|/dt|/dd)[^>]*>", "\n", s)
    s = re.sub(r"</?[a-zA-Z][^<>]*>", "", s)
    s = html.unescape(s)
    lines = [line.strip() for line in s.split("\n") if line.strip()]
    (out / f"L0{i}.txt").write_text("\n".join(lines), encoding="utf-8")
