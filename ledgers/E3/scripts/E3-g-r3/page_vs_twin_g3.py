"""For L05-L08: each lab twin's source must appear verbatim (after HTML unescape) in its page,
and the page's expected-output block must equal the twin's stdout captured in twin_Lnn.r3.out.
Usage: python -I page_vs_twin_g3.py <checkout> <scripts_dir>
"""
import html
import re
import sys

root, scripts = sys.argv[1], sys.argv[2]
for L in ("05", "06", "07", "08"):
    page = open(f"{root}/course/modules/E/E3/L{L}.html", encoding="utf-8").read()
    twin = open(f"{root}/tests/labs/E3/lab-E3-L{L}-1.py", encoding="utf-8").read()
    out = open(f"{scripts}/twin_L{L}.r3.out", encoding="utf-8").read()
    blocks = [html.unescape(re.sub(r"<[^>]+>", "", b)) for b in re.findall(r"<pre[^>]*>(.*?)</pre>", page, re.S)]
    code_ok = any(twin.strip() in b for b in blocks)
    out_ok = any(out.strip() == b.strip() for b in blocks)
    print(f"L{L}: twin source verbatim in page = {code_ok}; expected output block equals twin stdout = {out_ok}; "
          f"pre blocks = {len(blocks)}")
