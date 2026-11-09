"""Round 15, FC1-c: re-derive every number stated in the project page and the grader docstrings (python -I)."""

from decimal import Decimal, getcontext, localcontext, ROUND_HALF_EVEN
from fractions import Fraction as F
import math

def half_away(x):
    m = abs(x)
    w = math.floor(m + F(1, 2))
    return w if x >= 0 else -w

def price(events, yb):
    y = F(yb, 10000)
    return half_away(sum((F(a) / (1 + y) ** t for t, a in events), F(0)))

def ev(face, bps, n):
    c = half_away(F(face * bps, 10000))
    r = [(t, c) for t in range(1, n + 1)]
    r[-1] = (n, r[-1][1] + face)
    return r

print("L1 exact PV 102775.091033 ->", f"{float(sum((F(a)/(1+F(400,10000))**t for t,a in ev(100000,500,3)), F(0))):.6f}", price(ev(100000,500,3),400))
print("Fixture B exact 210000/19 ->", f"{float(F(210000,19)):.4f}", float(F(10500)/F(95,100)), price(ev(10000,500,1),-500))
print("Fixture A price ->", price(ev(10000,500,1),500))
print("Fixture C events ->", ev(10001,5000,2))
print("Fixture D events ->", ev(1,5000,1))
print("Fixture F price 1/2 -> round()", round(F(1,2)), "half_away", price(ev(1,0,1),10000))
print("Fixture G price 5000.5 ->", price(ev(10001,0,1),10000))
print("Rounding fixture exact ->", f"{float(sum((F(a)/(1+F(400,10000))**t for t,a in ev(10000,500,3)), F(0))):.6f}", price(ev(10000,500,3),400))
print("Rounding fixture terms ->", [f"{float(F(a)/(1+F(400,10000))**t):.2f}" for t,a in ev(10000,500,3)], [half_away(F(a)/(1+F(400,10000))**t) for t,a in ev(10000,500,3)])
print("496 bps exact ->", F(1734792)/F(10496,10000), price(ev(1704285,179,1),496), "float:", 1734792/(1+496/10000))
print("13/1.04 float path ->", (1+0.04)**-1*13, price([(1,13)],400))
print("10^10+1 ->", price([(1,10**10+1)],10000), "10^12+1 ->", price([(1,10**12+1)],10000), "10^40+1 ->", price([(1,10**40+1)],10000), 5*10**39+1)
with localcontext() as c:
    c.prec = 10
    print("prec-10 decimal drops half ->", Decimal("5000000000.5") + 0, Decimal(5000000000.5) if False else "", )
    print("prec10 round of 5000000000.5:", +Decimal("5000000000.5"), "| 500000000000.5:", +Decimal("500000000000.5"))
base = F(300075005)
ex = base / (F(10001, 10000)) ** 3
print("just-under: exact - 299985000 == 1/2 - 1/(2*1000300030001):", ex - 299985000 == F(1,2) - F(1, 2 * 1000300030001), "rounds to", price([(1,0),(2,0),(3,300075005)],1))
print("yield 16 decade: 10^30/(1+10^14) - 9999999999999900 == 100/(10^14+1):", F(10**30, 10**14+1) - 9999999999999900 == F(100, 10**14+1), price([(1,10**30)], 10**18))
print("150%:", price([(1,10500)],15000), "300%:", price([(1,10500)],30000), "2000%:", price([(1,10500)],200000), "10000%:", price([(1,10500)],1000000), "100000%:", price([(1,10500)],10000000))
print("1000 bps outside 50..900:", not (50 <= 1000 <= 900))
print("2^40+1 * 9851 > 2^53:", (2**40+1)*9851 > 2**53)
print("10^17+4999 coupon at 1 bps:", half_away(F((10**17+4999)*1, 10000)), 10**13, "events:", ev(10**17+4999,1,1))
print("1001 periods at 0 yield value:", price(ev(10000,0,1001),0))
print("Bond(10000,500,3) at 400bps round-up sanity 10278:", price(ev(10000,500,3),400))
print("Round 1/2 python:", round(F(1,2)))
print("float 1652812.4999999998 in python:", 1734792/(1.0496))
print("13 exact half equals 12.5:", F(13)/F(104,100) == F(25,2))
