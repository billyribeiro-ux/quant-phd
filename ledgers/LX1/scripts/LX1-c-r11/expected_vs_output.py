"""Compare each project-page expected block with the stdout of its twin (run alone, python -I -W error)."""
import html
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])  # checkout root
OUT = Path(sys.argv[2])   # directory holding out1.txt, out2.txt, out3.txt
page = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
print("expected blocks found:", len(blocks))
ok = True
for i, block in enumerate(blocks, 1):
    expected = html.unescape(block)
    actual = (OUT / f"out{i}.txt").read_text(encoding="utf-8")
    same = expected.rstrip("\n") == actual.rstrip("\n")
    ok &= same
    print(f"block {i}: lines expected={len(expected.splitlines())} output={len(actual.splitlines())} equal={same}")
    if not same:
        for a, b in zip(expected.splitlines(), actual.splitlines()):
            if a != b:
                print("  DIFF expected:", repr(a), "output:", repr(b))
print("ALL EQUAL" if ok else "MISMATCH")
