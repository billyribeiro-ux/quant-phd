from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().prec = 50
def A(r):
    return sum(F(1)/(1+r)**t for t in range(1,4))
for r in (F(8,100),F(10,100),F(12,100)):
    a = A(r)
    d = Decimal(a.numerator)/Decimal(a.denominator)
    print("rate", r, "A exact", str(d)[:20])
    be_exact = F(3000)/a
    print("  3000/A exact", str(Decimal(be_exact.numerator)/Decimal(be_exact.denominator))[:14])
    for digits in (7,8):
        # 7 significant digits and 7 decimals
        pass
    print("  A to 7 decimals", str(d.quantize(Decimal('0.0000001'), ROUND_HALF_UP)), " sig7:", '%.6e' % d)
# stated rounded factors
for s in ("2.5770970","2.4868520","2.4018313"):
    print("3000/",s,"=", str(Decimal(3000)/Decimal(s))[:14])
# using the seven-decimal factors as the page states
print("E1 check 1/1.12+1/1.2544+1/1.404928 =", str(sum(Decimal(1)/Decimal(x) for x in ("1.12","1.2544","1.404928"))))
print("  3000/that =", str(Decimal(3000)/sum(Decimal(1)/Decimal(x) for x in ("1.12","1.2544","1.404928")))[:14])
print("  3000/2.40183 =", str(Decimal(3000)/Decimal("2.40183"))[:12])
print("8pct 1/1.08 +..:", str(sum(Decimal(1)/Decimal(x) for x in ("1.08","1.1664","1.259712"))))
print("10pct:", str(sum(Decimal(1)/Decimal(x) for x in ("1.1","1.21","1.331"))))
be8=F(3000)/A(F(8,100)); be10=F(3000)/A(F(10,100)); be12=F(3000)/A(F(12,100))
print("diffs exact", float(be10-be8), float(be12-be10), float((be12-be8)/4))
print("diffs from 4dp", Decimal("1206.3444")-Decimal("1164.1005"), Decimal("1249.0469")-Decimal("1206.3444"), Decimal("1249.0469")-Decimal("1164.1005"))
print("84.9464/4", Decimal("84.9464")/4, "42.2439", "42.7025")
print("E2 1200 exact", F(5000*1200)*A(F(10,100)) - 15000000, float(F(5000*1200)*A(F(10,100)) - 15000000))
print("E2 1300 exact", float(F(5000*1300)*A(F(10,100)) - 15000000))
print("R3 m*", float(F(15000000)/(1600*A(F(10,100)))), float(F(15000000)/(1600*A(F(10,100)))/5000))
print("M3", F(33275,331), float(F(33275,331)), float(F(100000)/(400*A(F(10,100)))))
print("Q NPV M2", float(-100+F(60)/F(11,10)+F(60)/F(121,100)), F(500,121), float(F(500,121)))
