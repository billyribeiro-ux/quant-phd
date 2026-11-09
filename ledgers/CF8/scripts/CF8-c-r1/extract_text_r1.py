"""Plain-text dump of CF8 lessons for line-numbered evidence (read-only; writes into ledgers/CF8/scripts/CF8-c-r1/text/)."""
import html
import re

base = "course/modules/CF/CF8/"
for L in ["L01", "L02", "L03", "L04", "L05"]:
    raw = open(base + L + ".html", encoding="utf-8").read()
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.S)
    raw = re.sub(r"<br\s*/?>|</p>|</li>|</h[1-6]>|</div>|</pre>|</tr>", "\n", raw)
    text = html.unescape(re.sub(r"<[^>]+>", "", raw))
    lines = [line.rstrip() for line in text.split("\n") if line.strip()]
    with open("ledgers/CF8/scripts/CF8-c-r1/text/" + L + ".txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
print("ok")
