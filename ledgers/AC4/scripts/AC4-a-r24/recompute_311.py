"""Round 24: recompute the numbers in L02.html line 311 (misconception 3) from integer cents with Fractions."""
from fractions import Fraction

PRICE, VAR, FIXED, STEP, T = 2500, 1150, 120_000, 2_700_000, 2000  # cents; step above 2000 units
M = PRICE - VAR

def oi(q: int) -> int:
    return M * q - FIXED - (STEP if q > T else 0)

print("margin_cents", M, "ratio", Fraction(M, PRICE))
print("lower zero", float(Fraction(FIXED, M)))
print("upper zero", float(Fraction(FIXED + STEP, M)), "> T:", Fraction(FIXED + STEP, M) > T)
print("OI(2001) cents", oi(2001), "usd", oi(2001) / 100)
print("OI(2088) cents", oi(2088), "OI(2089) cents", oi(2089))
# Scope check: within the upper segment (T, inf), OI >= 0 exactly when Q >= upper zero
ok = all((oi(q) >= 0) == (q >= Fraction(FIXED + STEP, M)) for q in range(T + 1, 5001))
print("upper segment iff holds on 2001..5000:", ok)
# Within the lower segment [0, T], OI >= 0 exactly when Q >= lower zero
ok2 = all((oi(q) >= 0) == (q >= Fraction(FIXED, M)) for q in range(0, T + 1))
print("lower segment iff holds on 0..2000:", ok2)
# Plan of 2001 units is not in the lower segment: the lower zero alone does not decide its sign
print("2001 >= lower zero but OI < 0:", 2001 >= Fraction(FIXED, M) and oi(2001) < 0)
print("sensitivity 100 USD fixed:", float(Fraction(FIXED + 10_000, M) - Fraction(FIXED, M)))
