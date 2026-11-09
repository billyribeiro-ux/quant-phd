"""Strip HTML of a lesson page to numbered plain text lines (verifier helper)."""
import html
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
src = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", src)
src = re.sub(r"(?i)<br\s*/?>", "\n", src)
src = re.sub(r"(?i)</(p|div|li|tr|h[1-6]|pre|section|table|ul|ol|dt|dd|details|summary|thead|tbody)>", "\n", src)
src = re.sub(r"(?s)<(/?[a-zA-Z!][^>]*)>", "", src)
src = html.unescape(src)
for i, line in enumerate(src.split("\n"), 1):
    if line.strip():
        print(f"{i}: {line.strip()}")
