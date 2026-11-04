"""Round-3 scope scan: every block of L07/L08 that quotes a closed-form value or the closed form, listed with whether
its own text or the enclosing problem/quiz prompt names A3, A4, H2, A5 or 'assum'. Blocks without a qualifier are
printed for manual reading (solutions and answers inherit the qualifier of their prompt)."""
import html
import re
import sys

ROOT = sys.argv[1]
MARK = re.compile(r"0\.3173|0\.1586|0\.2419|0\.1098|0\.4795|0\.7978|closed form|erfc|2\s*\(1\s*-\s*\\Phi|2\(1-\\Phi|2\(1-\\Phi")
QUAL = re.compile(r"A3|H2|H1, H2|under H|Assuming|assum|A5")
for page in ("L07", "L08"):
    text = open(f"{ROOT}/course/modules/SC/SC1/{page}.html", encoding="utf-8").read()
    # split into prompt/solution units: problem divs, quiz items, prose blocks
    units = re.split(r'<div class="problem"|<li class="item"|<div class="block |<p class="why|<p>|<p class="interpretation"', text)
    for i, u in enumerate(units):
        plain = html.unescape(re.sub(r"<[^>]+>", " ", u))
        if MARK.search(plain) or MARK.search(u):
            flag = "qualified" if QUAL.search(plain) else "UNQUALIFIED"
            print(page, i, flag, "|", re.sub(r"\s+", " ", plain).strip()[:150])
print("scan complete")
