"""Compare each CS2 L05-L08 page's expected output block with the twin's stdout (verifier round 4).

Usage: python3 -I expected_vs_stdout_r4.py <checkout> <stdout-dir>
The page's expected block is the <pre> that follows the lab section's code block.
"""
import html
import re
import sys

root, outdir = sys.argv[1], sys.argv[2]
for n in (5, 6, 7, 8):
    page = open(f"{root}/course/modules/CS/CS2/L0{n}.html", encoding="utf-8").read()
    code_end = page.index("main()</code></pre>", page.index('data-run'))
    tail = page[code_end:]
    block = re.search(r"</code></pre>\s*<pre[^>]*>(.*?)</pre>", tail, re.S)
    if block is None:
        block = re.search(r"</code></pre>\s*(?:<pre[^>]*>)?(.*?)</pre>", tail, re.S)
    expected = html.unescape(re.sub(r"<[^>]+>", "", block.group(1))).strip().splitlines()
    got = open(f"{outdir}/out_L0{n}.txt", encoding="utf-8").read().strip().splitlines()
    print(f"L0{n}: expected lines {len(expected)} stdout lines {len(got)} equal={expected == got}")
    if expected != got:
        for a, b in zip(expected, got):
            if a != b:
                print("  page:", a)
                print("  twin:", b)
