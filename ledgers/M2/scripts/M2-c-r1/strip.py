"""Strip an HTML lesson to numbered text lines for reading (verifier scratch helper)."""
import html
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
src = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", "", src)
src = re.sub(r"(?i)<br\s*/?>", "\n", src)
src = re.sub(r"(?i)</(p|div|li|h[1-6]|tr|section|details|summary|figcaption|dt|dd|table|ol|ul|pre)>", "\n", src)
src = re.sub(r"(?i)<(tr|li|h[1-6]|section|details|figure|table)[^>]*>", "\n", src)
text = re.sub(r"</?[a-zA-Z][^>]*>", "", src)
text = html.unescape(text)
lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.split("\n")]
out = [ln for ln in lines if ln]
for i, ln in enumerate(out, 1):
    print(f"{i:04d} {ln}")
