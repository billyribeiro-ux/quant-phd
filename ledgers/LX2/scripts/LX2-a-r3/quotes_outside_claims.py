"""List quoted passages (curly double quotes) in a lesson page that sit outside any claim span, with line numbers.
Usage: python3 -I quotes_outside_claims.py <page.html>"""
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
# remove claim spans (non-nested in these pages; a claim span contains no nested span.claim)
stripped = re.sub(r'<span class="claim"[^>]*>.*?</span>', lambda m: "<CLAIM>" + ("\n" * m.group(0).count("\n")), src, flags=re.S)
for n, line in enumerate(stripped.split("\n"), 1):
    text = re.sub(r"<[^>]+>", "", line)
    for q in re.findall(r"“[^”]*”", text):
        print(f"{n}: {q[:160]}")
