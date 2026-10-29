# Compares the expected block of each L04-L06 page with the saved output of the twin run (python -I -W error).
import html, re, sys
ROOT = "/tmp/verifyB2-E1-b"
S = f"{ROOT}/ledgers/E1/scripts/E1-b-r2"
for n in ("04", "05", "06"):
    page = open(f"{ROOT}/course/modules/E/E1/L{n}.html", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(m.group(1)).strip().splitlines()
    got = open(f"{S}/twin-L{n}.out", encoding="utf-8").read().strip().splitlines()
    print(f"L{n}: page block {len(expected)} lines, twin output {len(got)} lines, identical: {expected == got}")
