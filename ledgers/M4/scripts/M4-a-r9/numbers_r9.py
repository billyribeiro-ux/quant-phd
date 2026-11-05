"""Round 9 slice a: recompute displayed numbers from unrounded values, and count why-it-matters words.

Run: python3 -I ledgers/M4/scripts/M4-a-r9/numbers_r9.py <checkout-root>
"""

import math
import re
import sys
from fractions import Fraction as F

root = sys.argv[1].rstrip("/")
print("sqrt(35/12) =", round(math.sqrt(F(35, 12)), 5), "-> 1.708 (L02 Ex 2.5)")
print("sqrt(2968750000) =", round(math.sqrt(2968750000), 4), "-> 54486.24 (L02 Ex 2.6)")
print("sqrt(296875) =", round(math.sqrt(296875), 4), "-> 544.8624 (L02 R2)")
print("sqrt(2968750000)/100 =", round(math.sqrt(2968750000) / 100, 4), "-> 544.8624 (L02 R2 via cents/100)")
m2, m3, m4 = F(163, 16), F(2157, 32), F(149461, 256)
print("E[X] =", F(7, 4), " m2 =", m2, " m3 =", m3, " m4 =", m4)
print("skew^2 exact =", m3 * m3 / m2**3, "=", float(m3 * m3 / m2**3))
print("skew =", round(float(m3) / float(m2) ** 1.5, 6), "-> 2.0730 (L03 lab) ; exact 2.073 line")
print("kurt exact =", m4 / m2**2, "=", round(float(m4 / m2**2), 6), "-> 5.6254 / 5.625 line")
print("gap skew (2.073 - 2.065) =", round(2.073 - 2.065, 6), " gap kurt (5.625 - 5.580) =", round(5.625 - 5.580, 6))
print("Bernoulli p=1/10: gamma3 =", (1 - 2 * F(1, 10)) / math.sqrt(F(9, 100)), " gamma4 =", (1 - 3 * F(9, 100)) / F(9, 100), "=", float((1 - 3 * F(9, 100)) / F(9, 100)))
print("Bernoulli p=1/4: gamma3 =", round(2 / math.sqrt(3), 4), " gamma4 =", (1 - 3 * F(3, 16)) / F(3, 16))
print("Bernoulli 2/5 pattern pq=1/6 gamma4 =", (1 - 3 * F(1, 6)) / F(1, 6))
print("8/3 =", round(8 / 3, 4), " 5/3 =", round(5 / 3, 4), " 73/9 =", round(73 / 9, 4), " 7/3 =", round(7 / 3, 4))
print("L04 ratio 1/10 over 4/25 =", F(1, 10) / F(4, 25), "; 1/3 over 1/9 =", F(1, 3) / F(1, 9))
print("0.99*150 =", 0.99 * 150, " ceil =", math.ceil(0.99 * 150), " 148/150 =", round(148 / 150, 4), " 74/75 =", round(74 / 75, 4))
print("0.99*200 =", 0.99 * 200, " 0.9*40 =", 0.9 * 40, " 0.901*40 =", round(0.901 * 40, 6))
print("E[X] for L01 Ex 3.6 =", sum(F(v) * F(k, 10) for v, k in [(-2, 1), (-1, 2), (0, 3), (1, 2), (2, 1), (3, 1)]))
print("Var(2X) die / Var(X) =", F(35, 3) / F(35, 12))
print("E[L^2] =", F(250000) ** 2 / 20, " Var(L) =", F(250000) ** 2 / 20 - F(12500) ** 2)
print("L02 Ex 2.6 cents sd rounded 2dp:", f"{math.sqrt(2968750000):.2f}")
print("seed-2027 expected losses =", 10000 / 20, "; 500-489 =", 500 - 489)
print("L04 Ex 2.5 E[X|Y=1] =", (F(2, 10) + F(2, 10)) / F(6, 10), "; E[X|Y=0] =", (F(2, 10) + F(2, 10)) / F(4, 10))
print("hub 0.833 check 5/6 =", round(5 / 6, 4), "; 1/(1+r) ok; 15/8 =", F(15, 8), float(F(15, 8)))
print("ceil(36.04)=", math.ceil(36.04), " 1/(1-1/sqrt3)/2 check pq =", round(((1 - 1 / math.sqrt(3)) / 2) * ((1 + 1 / math.sqrt(3)) / 2), 6))

print()
for lesson in ("L01", "L02", "L03", "L04"):
    text = open(f"{root}/course/modules/M/M4/{lesson}.html", encoding="utf-8").read()
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', text, re.S)
    body = re.sub(r"\\\((.*?)\\\)", r"\1", m.group(1))
    body = re.sub(r"<[^>]+>", " ", body)
    print(lesson, "why-it-matters words =", len(body.split()))
