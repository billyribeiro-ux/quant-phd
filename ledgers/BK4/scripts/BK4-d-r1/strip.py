# Strip HTML of a BK4 lesson to readable text, keeping line structure, for the cards slice verification.
import html
import re
import sys

src = sys.argv[1]
text = open(src, encoding="utf-8").read()
text = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", text)
text = re.sub(r"(?i)<br\s*/?>", "\n", text)
text = re.sub(r"(?i)</(p|div|li|tr|h[1-6]|pre|dt|dd|table|section|ul|ol|blockquote)>", "\n", text)
text = re.sub(r"(?i)<(td|th)\b[^>]*>", " | ", text)
text = re.sub(r"<(?=/?[A-Za-z!])[^>]*>", "", text)
text = html.unescape(text)
lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.split("\n")]
out = []
for ln in lines:
    if ln:
        out.append(ln)
sys.stdout.write("\n".join(out) + "\n")
