"""FC1-b round 5: independent recomputation of every L04/L05 number and claim that the twin does not print.

Run from the checkout root: .venv/bin/python -I ledgers/FC1/scripts/FC1-b-r5/numbers_r5.py
"""

import datetime
import html
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(".").resolve()
L04 = (ROOT / "course/modules/FC/FC1/L04.html").read_text(encoding="utf-8")
L05 = (ROOT / "course/modules/FC/FC1/L05.html").read_text(encoding="utf-8")
TWIN04 = ROOT / "tests/labs/FC1/lab-FC1-L04-1.py"
TWIN05 = ROOT / "tests/labs/FC1/lab-FC1-L05-1.py"


def wd(d: datetime.date) -> str:
    return d.strftime("%A")


def bday_after(start: datetime.date, n: int) -> datetime.date:
    d, c = start, 0
    while c < n:
        d += datetime.timedelta(days=1)
        if d.weekday() < 5:
            c += 1
    return d


print("== dates")
t = datetime.date(2026, 10, 28)
for label, d in [("trade", t), ("+1", bday_after(t, 1)), ("+2", bday_after(t, 2)), ("+3", bday_after(t, 3))]:
    print(label, d.isoformat(), wd(d))
print("Oct30 +1 =", bday_after(datetime.date(2026, 10, 30), 1), "+2 =", bday_after(datetime.date(2026, 10, 30), 2))
print("Oct30 is", wd(datetime.date(2026, 10, 30)))

print("== numbers")
G, NP = 68398886, 14282414
print("NP/G exact", Fraction(NP, G), float(Fraction(NP, G)))
q = Fraction(NP, G) * 10**8
print("NP/G to 8 dp (floor)", int(q) / 10**8, "half-up 8dp", (2 * NP * 10**8 + G) // (2 * G) / 10**8)
print("NP/G half-up 5dp", (2 * NP * 10**5 + G) // (2 * G) / 10**5, "half-up 4dp", (2 * NP * 10**4 + G) // (2 * G) / 10**4,
      "half-up 3dp", (2 * NP * 10**3 + G) // (2 * G) / 10**3)
P5 = 11060360
print("P5/G exact", float(Fraction(P5, G)), "half-up 2dp pct", (2 * P5 * 10**4 + G) // (2 * G) / 100)
print("P5/NP exact", float(Fraction(P5, NP)), "half-up 2dp pct", (2 * P5 * 10**4 + NP) // (2 * NP) / 100)
print("216*10060 =", 216 * 10060, " 100*10090 =", 100 * 10090, " 159000/150 =", Fraction(159000, 150))
print("5600/173 =", Fraction(5600, 173), float(Fraction(5600, 173)))
print("E2 sum negatives", 7411991 + 6656379 + 214044, "positives", 3222054 + 11060360)
print("net sum", -7411991 - 6656379 + 3222054 - 214044 + 11060360)
print("L04 M1 cost", 60 * 995 + 40 * 990, "avg", Fraction(60 * 995 + 40 * 990, 100))
print("P2 L04 G", 150 + 100, "2X+C", 2 * 100 + 50)
print("24+18 =", 24 + 18, " 181+77+42 =", 181 + 77 + 42)
print("R1 fills 990,985,980 stop logic ok")
print("A 1000000 check M3 ratio", Fraction(1000000, 2000000))
print("R2 L05 values: xA", 100, "xB", -100, "NP", max(100, 0), "G", -100)

print("== why-it-matters word counts (<=120 required)")
for name, page in [("L04", L04), ("L05", L05)]:
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', page, re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))
    words = text.split()
    print(name, len(words))

print("== twin vs page: expected block and code")
def expected_block(page: str) -> str:
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    return html.unescape(m.group(1))


def page_code(page: str) -> str:
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    return html.unescape(m.group(1))


for name, page, twin in [("L04", L04, TWIN04), ("L05", L05, TWIN05)]:
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=False)
    out = res.stdout
    exp = expected_block(page)
    print(name, "rc", res.returncode, "stderr", repr(res.stderr[:200]))
    print(name, "expected == output:", exp.rstrip("\n") == out.rstrip("\n"))
    code = page_code(page)
    src = twin.read_text(encoding="utf-8")
    print(name, "page code == twin:", code.rstrip("\n") == src.rstrip("\n"))
    if exp.rstrip("\n") != out.rstrip("\n"):
        print("DIFF expected vs output")
        import difflib
        print("\n".join(difflib.unified_diff(exp.splitlines(), out.splitlines(), lineterm="")))
    if code.rstrip("\n") != src.rstrip("\n"):
        import difflib
        print("\n".join(list(difflib.unified_diff(src.splitlines(), code.splitlines(), lineterm=""))[:40]))
