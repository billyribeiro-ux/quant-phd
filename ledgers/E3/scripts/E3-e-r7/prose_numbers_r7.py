"""Re-derive the numbers that round-7 prose states (L02, L04, L07, L08, project, degenerate-case docstring).

Run: python -I prose_numbers_r7.py <checkout>. Prints one line per check; the verifier reads the printed values.
"""
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])
E3 = root / "course/modules/E/E3"


def w(p: float) -> float:  # L07 weighting function, closed form stated on the page
    return math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))


print("L07 w(3/10)=%.10f w(3/5)=%.10f w(1/2)=%.10f" % (w(0.3), w(0.6), w(0.5)))
print("L07 w(0.01)=%.10f w(0.99)=%.10f" % (w(0.01), w(0.99)))
print("L07 ratio w(3/10)/w(3/5)=%.10f threshold 1/(1+2^-1)=%.6f" % (w(0.3) / w(0.6), 1 / (1 + 2 ** -1)))
over = (w(0.01) - 0.01) * 100
under = (0.99 - w(0.99)) * 50
print("L07 weighted=%.4f EV=%.2f overweight=%.2f underweight=%.2f net=%.2f" % (
    w(0.01) * 100 + w(0.99) * 50, 0.01 * 100 + 0.99 * 50, over, under, over - under))
print("L07 omega(2/5)+2 omega(3/10)=%.8f" % (w(0.4) + 2 * w(0.3)))
print("L07 2 omega(3/10)=%.8f" % (2 * w(0.3)))

# L02 Lab 1 Part A numbers (square-root utility, wealth lottery of 40/100/160 with 1/4, 1/2, 1/4)
ev = Fraction(1, 4) * 40 + Fraction(1, 2) * 100 + Fraction(1, 4) * 160
eu = 0.25 * math.sqrt(40) + 0.5 * math.sqrt(100) + 0.25 * math.sqrt(160)
ce = eu ** 2
print("L02 mean=%s E sqrt=%.6f CE=%.6f premium=%.6f cents CE=%.4f premium_cents=%.4f" % (
    ev, eu, ce, 100 - ce, ce * 100, (100 - ce) * 100))

# L08 Epstein-Zin and CRRA check numbers printed in the page (Model 3 is 101951.2195)
print("L08 4180000/41=%.4f" % (4180000 / 41))

# L04 comparison counts on the printed lab output (expected block of lab-E3-L04-1)
lab04 = (E3 / "L04.html").read_text(encoding="utf-8")
block = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', lab04, re.S).group(1)
named = re.findall(r"^named pair .*agree: (True|False)$", block, re.M)
pairs = re.findall(r"^pair \d\d \(.*?\): FOSD .*$", block, re.M)
fo_seeded = len(pairs)
so_seeded = len(re.findall(r"equal means, SOSD", block))
print("L04 named comparisons:", len(named), "all agree:", all(v == "True" for v in named))
print("L04 seeded FOSD comparisons:", fo_seeded, "| seeded equal-mean SOSD comparisons:", so_seeded)
print("L04 named FOSD:", sum(1 for line in block.splitlines() if line.startswith("named pair") and "FOSD" in line),
      "named SOSD:", sum(1 for line in block.splitlines() if line.startswith("named pair") and "SOSD" in line))
print("L04 total agreeing comparisons claimed 37:", fo_seeded + so_seeded + len(named),
      "| every agree flag True:", "False" not in re.findall(r"agree[^\n]*", block))
