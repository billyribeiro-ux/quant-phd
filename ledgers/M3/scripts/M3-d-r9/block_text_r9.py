"""Round-9 verifier helper: print the statement text that follows a named block title in an M3 lesson (for card checks)."""
import html
import re
import sys
from pathlib import Path

lesson, labels = sys.argv[1], sys.argv[2:]
text = Path(f"course/modules/M/M3/{lesson}.html").read_text(encoding="utf-8")
for label in labels:
    m = re.search(r'<span class="block-title[^"]*"[^>]*>' + re.escape(label) + r' <span class="name">(.*?)</span></span>', text, re.S)
    if not m:
        print(f"== {lesson} {label}: NOT FOUND")
        continue
    name = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    body = text[m.end(): m.end() + 2500]
    body = re.split(r'<span class="block-title', body)[0]
    body = html.unescape(re.sub(r"<[^>]+>", " ", body))
    body = re.sub(r"\s+", " ", body).strip()
    print(f"== {lesson} {label} ({name}): {body[:520]}")
