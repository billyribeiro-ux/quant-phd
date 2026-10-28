"""Dump plain text of named blocks from a CF1 lesson. Usage: python -I dump_blocks_r7.py <lesson.html> <label-prefix>... """
import html
import re
import sys

text = open(sys.argv[1]).read()
for prefix in sys.argv[2:]:
    for m in re.finditer(r'<div class="block[^"]*">\s*<span class="block-title[^>]*>\s*' + re.escape(prefix), text):
        seg = text[m.start(): m.start() + 3000]
        end = seg.find("</div>\n      </div>")
        seg = seg[: end] if end > 0 else seg[:1500]
        plain = re.sub(r"<[^>]+>", "", seg)
        plain = html.unescape(re.sub(r"\s+", " ", plain)).strip()
        print("##", plain[:900])
        print()
