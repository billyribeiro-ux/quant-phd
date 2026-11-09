"""Round-18 LX1-c: exact Fraction recomputation of the Lab 1 and Lab 2 numbers stated on project.html (verifier-written)."""
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

def q(x, places=2):
    return Decimal(x.numerator) / Decimal(x.denominator) if False else (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)

fall = [F(p, 100) for p in (100, 97, 94, 91, 88, 85)]
rise = [F(p, 100) for p in (100, 103, 106, 109, 112, 115)]
D = F(100000)
print("Lab1 real debt falling:", [str(q(D / p)) for p in fall])
print("Lab1 real debt rising:", [str(q(D / p)) for p in rise])
print("Lab1 burden falling %:", q(100 * (fall[0] / fall[-1] - 1)), " rising %:", q(100 * (rise[0] / rise[-1] - 1)))
print("Lab1 Part C difference $:", q(D / fall[-1] - D / rise[-1]), " exact cents:", float((D / fall[-1] - D / rise[-1]) * 100))
print("Lab1 period-5 exact cents falling:", float(D * 100 / fall[-1]), " rising:", float(D * 100 / rise[-1]))
p2 = [F(p, 100) for p in (100, 99, 98, 96, 95, 93)]
D2 = F(40000)
print("Lab2 real debt:", [str(q(D2 / p)) for p in p2])
print("Lab2 burden %:", q(100 * (p2[0] / p2[-1] - 1)))
print("Lab2 inverted burden %:", q(100 * (p2[-1] / p2[0] - 1)))
print("Lab1 burden with the period-5 real value as base (wrong) %:", q(100 * (D / fall[-1] / (D / fall[0]) - 1)))
