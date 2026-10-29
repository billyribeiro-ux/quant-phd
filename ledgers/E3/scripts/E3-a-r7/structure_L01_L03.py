"""List block titles and section headings of E3 L01-L03 (python -I)."""
import html
import re
import sys
from pathlib import Path

for lid in ("L01", "L02", "L03"):
    text = Path(sys.argv[1], f"course/modules/E/E3/{lid}.html").read_text(encoding="utf-8")
    print("==", lid)
    for m in re.finditer(r'<(h2|h3)[^>]*>(.*?)</\1>', text, re.S):
        print("  H", re.sub(r"<[^>]+>", "", m.group(2)).strip()[:90])
    for m in re.finditer(r'<span class="block-title[^"]*"[^>]*>(.*?)</span>\s*(?:<span class="name">(.*?)</span>)?', text, re.S):
        t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        n = re.sub(r"<[^>]+>", "", m.group(2) or "").strip()
        print("  B", t, n[:70])
