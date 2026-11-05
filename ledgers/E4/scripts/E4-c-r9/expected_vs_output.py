"""Round 9, slice E4-c: compare each page's expected block with the captured stdout of its twin (exact line equality)."""
import html
import re
import sys

BASE = "/Users/billyribeiro/.fanout/wt/verifyE9-E4-c/"
OUT = BASE + "ledgers/E4/scripts/E4-c-r9/out/"
ok = True
for lesson in ("L07", "L08", "L09"):
    with open(BASE + "course/modules/E/E4/" + lesson + ".html", encoding="utf-8") as fh:
        src = fh.read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(m.group(1)).strip("\n").splitlines()
    with open(OUT + "twin_" + lesson + "-1.out", encoding="utf-8") as fh:
        got = [line for line in fh.read().splitlines() if not line.startswith("exit=")]
    same = expected == got
    ok = ok and same
    print(lesson, "expected lines", len(expected), "output lines", len(got), "identical", same)
sys.exit(0 if ok else 1)
