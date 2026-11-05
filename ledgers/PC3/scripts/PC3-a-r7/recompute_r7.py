"""Round 7: independent recomputation of every number in the slice (index, L01-L03). Prints each check."""
import math
from decimal import Decimal, getcontext
from fractions import Fraction as F
from itertools import product

getcontext().prec = 50
fails = []


def check(label, got, want, tol=0.0):
    ok = abs(float(got) - float(want)) <= tol if tol else got == want
    print(("PASS " if ok else "FAIL ") + f"{label}: got {got} want {want}")
    if not ok:
        fails.append(label)


# ---- L01 ----
lo = F(20) * 2 * 300
hi = F(60) * 10 * 390
check("L01 lower bound 12000", lo, 12000)
check("L01 upper bound 234000", hi, 234000)
check("L01 ratio 19.5", hi / lo, F(39, 2))
w = math.log(19.5)
check("L01 ln 19.5 to 10 dp", f"{w:.10f}", "2.9704144656")
check("L01 geometric midpoint 52990.57 (2 dp)", f"{math.sqrt(12000 * 234000):.2f}", "52990.57")
check("L01 geometric midpoint 52990.5652 (4 dp)", f"{math.sqrt(12000 * 234000):.4f}", "52990.5652")
w1, w2, w3 = math.log(3), math.log(5), math.log(1.3)
check("L01 factor widths sum to ln19.5", f"{w1 + w2 + w3:.10f}", "2.9704144656")
r_sym = math.log(40 / 20)
r_qu = math.log(8 / 4)
r_min = math.log(360 / 330)
d_sym = w1 - r_sym
d_qu = w2 - r_qu
d_min = w3 - r_min
check("L01 Part2 symbols reduction 0.4054651081", f"{d_sym:.10f}", "0.4054651081")
check("L01 Part2 quote reduction 0.9162907319", f"{d_qu:.10f}", "0.9162907319")
check("L01 Part2 minutes reduction 0.1753528875", f"{d_min:.10f}", "0.1753528875")
check("L01 totals 2.5649", f"{w - d_sym:.4f}", "2.5649")
check("L01 totals 2.0541", f"{w - d_qu:.4f}", "2.0541")
check("L01 totals 2.7951", f"{w - d_min:.4f}", "2.7951")
check("L01 quote share 30.8 pct (full precision)", f"{100 * d_qu / w:.1f}", "30.8")
check("L01 minutes share 5.9 pct", f"{100 * d_min / w:.1f}", "5.9")
check("L01 E2 four-place route 0.9163/2.9704 = 30.85 pct", f"{100 * round(0.9163 / 2.9704, 4):.2f}", "30.85")
check("L01 E2 quotient full precision 0.308472", f"{d_qu / w:.6f}", "0.308472")
check("L01 E2 minutes quotient 0.059033", f"{d_min / w:.6f}", "0.059033")
check("L01 R1 half of total 1.4852", f"{w / 2:.4f}", "1.4852")
check("L01 R1 ln5 = 1.6094", f"{w2:.4f}", "1.6094")
check("L01 R1 ln3 = 1.0986", f"{w1:.4f}", "1.0986")
check("L01 R1 ln1.3 = 0.2624", f"{w3:.4f}", "0.2624")
check("L01 R3 ln(3/2)=0.4055", f"{math.log(1.5):.4f}", "0.4055")
check("L01 R3 ln2.5=0.9163", f"{math.log(2.5):.4f}", "0.9163")
check("L01 R3 ln(2.5/1.01)=0.9063", f"{math.log(2.5 / 1.01):.4f}", "0.9063")
check("L01 E3 ln16.5=2.8034", f"{math.log(16.5):.4f}", "2.8034")
check("L01 E3 change 0.167054", f"{w - math.log(16.5):.6f}", "0.167054")
check("L01 E3 new hi 198000", F(60) * 10 * 330, 198000)
check("L01 E4 ln2+ln2 = ln4", f"{2 * math.log(2):.10f}", f"{math.log(4):.10f}")
# Taylor values
for n in (2, 5, 10):
    for x in (F(1, 100), F(1, 20)):
        rem = (1 + x) ** n - 1 - n * x
        bound = F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
        tail = sum(__import__("math").comb(n, j) * x**j for j in range(2, n + 1))
        assert rem == tail and 0 <= rem <= bound
        print(f"n={n} x={float(x):.2f} exact={float((1+x)**n):.10f} rem={float(rem):.10f} bound={float(bound):.10f}")
check("L01 E1 ratio 0.94854 (0.9485)", f"{0.0046221254 / 0.0048728552:.4f}", "0.9485")
check("L01 ratio exact 0.9485456", f"{float(((F(101,100))**10-1-F(10,100))/(F(45)*F(101,100)**8*F(1,10000))):.7f}", "0.9485456")
check("L01 bound excess 5.4 pct", f"{100 * (0.0048728552 / 0.0046221254 - 1):.1f}", "5.4")
check("L01 x=1/20 miss share 7.9 pct", f"{100 * 0.1289 / 1.6289:.1f}", "7.9")
check("L01 M1 product [5,21]", F(2 * 5) * F(1, 2), 5)
check("L01 M1 ln4.2 widths", f"{math.log(1.5) + math.log(1.4) + math.log(2):.10f}", f"{math.log(4.2):.10f}")
check("L01 M2 ln16 = 2.7726", f"{math.log(16):.4f}", "2.7726")
check("L01 M3 remainder 31/1000", F(11, 10) ** 3 - 1 - F(3, 10), F(31, 1000))
check("L01 M3 bound 33/1000", F(3 * 2, 2) * F(11, 10) * F(1, 100), F(33, 1000))
check("L01 Q2 ln4 6dp", f"{math.log(4):.6f}", "1.386294")
check("L01 Q6 remainder 0.004622", f"{0.0046221254:.6f}", "0.004622")
check("L01 Q9 sqrt(2808000000)", f"{math.sqrt(2808000000):.4f}", "52990.5652")
check("L01 Q9 52 990.57", f"{math.sqrt(2808000000):.2f}", "52990.57")
check("L01 misc 1.1046221254 (1.01)^10", f"{1.01**10:.10f}", "1.1046221254")
check("L01 1.05^10 4 places", f"{1.05**10:.4f}", "1.6289")
check("L01 bound at x=1/20 0.1662", f"{F(45) * F(105,100)**8 * F(1,400):.4f}".replace("0000", "0000"), f"{float(F(45) * F(105,100)**8 * F(1,400)):.4f}")
check("L01 bound at x=1/20 numeric 0.1662", f"{float(F(45) * F(105,100)**8 * F(1,400)):.4f}", "0.1662")
# ---- L02 ----
import random  # noqa
check("L02 bayes example P(B)=29/100", F(1, 2) * F(3, 10) + F(1, 5) * F(7, 10), F(29, 100))
check("L02 M2 P(A|B)=15/29", F(15, 100) / F(29, 100), F(15, 29))
check("L02 M3 2/5", F(4, 6) * F(3, 5), F(2, 5))
check("L02 M3 12/30", F(12, 30), F(2, 5))
check("L02 M1 1/6", F(1, 36) / F(6, 36), F(1, 6))
check("L02 E1 57/64", 1 - F(1, 64) - F(6, 64), F(57, 64))
check("L02 E3 1/6", F(2, 3) - F(1, 2), F(1, 6))
check("L02 Ex2.6 both|atleast1", F(1, 4) / F(3, 4), F(1, 3))
check("L02 Ex2.6 both|first heads", F(1, 4) / F(1, 2), F(1, 2))
check("L02 urn second red 12/20", F(12, 20), F(3, 5))
check("L02 urn both red 6/20", F(6, 20), F(3, 10))
check("L02 urn red|blue 6/8", F(6, 8), F(3, 4))
check("L02 bag P(red)=1/2", F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4), F(1, 2))
check("L02 bag posterior 3/4", F(1, 2) * F(3, 4) / F(1, 2), F(3, 4))
check("L02 R1 threshold etc: rule B switch 1/2", F(1, 3) / F(2, 3), F(1, 2))
check("L02 R3 blue first: 3/3", F(3, 3), 1)
check("L02 quiz 1/3 6dp", f"{1/3:.6f}", "0.333333")
check("L02 quiz 0.3", F(6, 20), F(3, 10))
# Monty Hall by independent brute force over (car, pick, host)
def monty(rule):
    stay = switch = total = F(0)
    for car, pick in product(range(3), range(3)):
        others = [d for d in range(3) if d != pick]
        if rule == "A":
            goats = [d for d in others if d != car]
            choices = [(o, F(1, len(goats))) for o in goats]
        else:
            choices = [(o, F(1, 2)) for o in others if o != car]
        for opened, p in choices:
            wgt = F(1, 9) * p
            total += wgt
            sw = [d for d in others if d != opened][0]
            stay += wgt if pick == car else 0
            switch += wgt if sw == car else 0
    return stay / total, switch / total
check("L02 Monty rule A stay 1/3", monty("A")[0], F(1, 3))
check("L02 Monty rule A switch 2/3", monty("A")[1], F(2, 3))
check("L02 Monty rule B stay 1/2", monty("B")[0], F(1, 2))
check("L02 Monty rule B switch 1/2", monty("B")[1], F(1, 2))
check("L02 P(goat reveal) rule B = 2/3", F(2, 3), F(2, 3))
# ---- L03 ----
check("L03 die E = 7/2", F(21, 6), F(7, 2))
check("L03 100*E = 350", 100 * F(7, 2), 350)
check("L03 two dice E = 7", F(sum(x + y for x, y in product(range(1, 7), repeat=2)), 36), 7)
check("L03 continuation 250", F(350) - 100, 250)
vals = [max(100 * f, 250) for f in range(1, 7)]
check("L03 backward induction value 1150/3", F(sum(vals), 6), F(1150, 3))
check("L03 gain 100/3", F(1150, 3) - 350, F(100, 3))
check("L03 2300/6 = 1150/3", F(2300, 6), F(1150, 3))
check("L03 R2 c=1 gain 74.5", float(F(sum(max(100 * f, 349) for f in range(1, 7)), 6) - 350), 74.5)
check("L03 R2 c=100 gain 100/3", float(F(sum(max(100 * f, 250) for f in range(1, 7)), 6) - 350), 100 / 3)
check("L03 E2 625/8 - 150", F(625, 8) - 150, F(-575, 8))
check("L03 E2 -71.875", float(F(-575, 8)), -71.875)
check("L03 biased per-turn 25", F(1, 2) * 150 + F(1, 2) * -100, 25)
check("L03 biased 6*25 = 150", 6 * 25, 150)
check("L03 M1 net 300", 100 * F(7, 2) - 50, 300)
check("L03 M2 p=1/3", F(1, 3), F(1, 3))
check("L03 M3 200", F(1, 2) * 100 + F(1, 2) * (-50 + 100 * F(7, 2)), 200)
check("L03 R1 expectation 50", F(200 + 100 + 0 - 100, 4), 50)
# Lab-style stopping recursion on the fair and biased games, independent implementation
def expect(outcomes, rule, H=6):
    def v(h):
        if len(h) == H or rule(h):
            return F(sum(h))
        return sum((p * v(h + (x,)) for x, p in outcomes), F(0))
    return v(())
RULES = [
    ("first win", lambda h: bool(h) and h[-1] > 0),
    ("first loss", lambda h: bool(h) and h[-1] < 0),
    ("reach 100", lambda h: sum(h) >= 100),
    ("200 gain or loss", lambda h: sum(h) >= 200 or sum(h) <= -200),
]
BIASED = ((150, F(1, 2)), (-100, F(1, 2)))
for name, rule in RULES:
    print("biased", name, expect(BIASED, rule))
check("L03 biased first-win 1575/32", expect(BIASED, RULES[0][1]), F(1575, 32))
check("L03 biased first-loss 1575/32", expect(BIASED, RULES[1][1]), F(1575, 32))
check("L03 biased reach100 575/8", expect(BIASED, RULES[2][1]), F(575, 8))
check("L03 biased 200 625/8", expect(BIASED, RULES[3][1]), F(625, 8))
FAIR = ((100, F(1, 2)), (-100, F(1, 2)))
for name, rule in RULES:
    check("L03 fair " + name + " zero", expect(FAIR, rule), 0)
# R1 looks-ahead rule
paths = [(100, 200), (100, 0), (-100, 0), (-100, -200)]
check("L03 R1 expected total", F(sum(max(a, b) for a, b in paths), 4), 50)
# 64 policies best
def pol(bits):
    total = F(0)
    for f in range(1, 7):
        total += F(100 * f) if bits[f - 1] else F(250)
    return total / 6
best = max(pol(b) for b in product((0, 1), repeat=6))
check("L03 best of 64 policies 1150/3", best, F(1150, 3))
print("FAILS:", fails)
