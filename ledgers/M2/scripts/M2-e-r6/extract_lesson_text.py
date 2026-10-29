"""Write plain text of each M2 lesson (L01..L24) to a directory, so each card can be checked against its lesson.
Run: python extract_lesson_text.py <repo_root> <out_dir>"""
import html
import re
import sys
from pathlib import Path

mod = Path(sys.argv[1]) / "course/modules/M/M2"
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for n in range(1, 25):
    raw = (mod / f"L{n:02d}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r'<pre class="expected".*?</pre>', lambda m: "[EXPECTED] " + html.unescape(re.sub(r"<[^>]+>", "", m.group(0))), raw, flags=re.S)
    raw = re.sub(r"<(br|/p|/li|/h[1-6]|/pre|/tr|/div)[^>]*>", "\n", raw)
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    (out / f"L{n:02d}.txt").write_text(t, encoding="utf-8")
print("wrote", out)
