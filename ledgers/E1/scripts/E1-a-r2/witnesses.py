"""Witnesses for round-2 rows (standard library only)."""
from fractions import Fraction as F
# L03 'need not be unique' witness: D(p)=2-p (strictly decreasing), S(p)=2|p-1| (continuous, not monotone)
Z = lambda p: (2 - p) - 2 * abs(p - 1)
print("L03 witness zeros:", [p for p in (F(0), F(4, 3)) if Z(p) == 0], "Z(0)=", Z(F(0)), "Z(4/3)=", Z(F(4, 3)))
# L02 why-it-matters witness: p=1, c=3, k=1, F=0 -> q*=max(0,(p-c)/(2k))=0, MC(0)=c=3 != p=1
p, c, k = F(1), F(3), F(1)
qstar = max(F(0), (p - c) / (2 * k))
print("L02 witness q*:", qstar, "MC(q*):", c + 2 * k * qstar, "price:", p)
# L02 R2 hidden differentiability: q*(p) from the FOC MC(q)=p is differentiable for p>c; check the envelope numerically
def pistar(pp, cc=F(2), kk=F(1), FF=F(12)):
    return (pp - cc) ** 2 / (4 * kk) - FF
h = F(1, 10**6)
print("L02 R2 envelope check dpi*/dp at p=10 ~", float((pistar(F(10) + h) - pistar(F(10) - h)) / (2 * h)), "q*(10)=", (F(10) - 2) / 2)
