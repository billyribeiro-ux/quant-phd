"""Strict diff of each L05-L08 page's expected block against the stdout of its twin run under python -I -W error.

Usage: python3 -I twin_strict_diff.py <checkout> <outdir-with-out.txt-per-lesson>. Run each twin first into <outdir>/L0n/out.txt.
"""
import html
import re
import sys

root, outdir = sys.argv[1], sys.argv[2]
for n in (5, 6, 7, 8):
    page = open(f"{root}/course/modules/E/E3/L0{n}.html", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = [l.rstrip() for l in html.unescape(m.group(1)).strip("\n").split("\n")]
    out = [l.rstrip() for l in open(f"{outdir}/L0{n}/out.txt", encoding="utf-8").read().strip("\n").split("\n")]
    diff = [i for i, (a, b) in enumerate(zip(exp, out)) if a != b]
    print(f"L0{n}: expected {len(exp)} lines, output {len(out)} lines, differing {len(diff)}")
