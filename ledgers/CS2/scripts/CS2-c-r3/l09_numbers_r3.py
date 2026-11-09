"""Independent recomputation of every L09 number (CS2-c r3). Reads the twin, drops its final main() call, reuses nothing else."""
import math
import sys
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 80
src = open(sys.argv[1], encoding="utf-8").read()
src = src.rsplit("\nmain()", 1)[0]
ns: dict = {}
exec(compile(src, "twin", "exec"), ns)
stream, welford, two_pass, naive, exact_variance, relative_error = (
    ns["stream"], ns["welford_variance"], ns["two_pass_variance"], ns["naive_variance"],
    ns["exact_variance"], ns["relative_error"])

for off in (0.0, 1e6, 1e9):
    xs = stream(off)
    ex = exact_variance(xs)
    print("offset", repr(off), "exact", float(ex), "exact Fraction 12dp", f"{float(ex):.12f}")
    print("  unrounded exact (Decimal 20dp)", Decimal(ex.numerator) / Decimal(ex.denominator))
    for name, m in (("welford", welford), ("two-pass", two_pass), ("naive", naive)):
        est = m(xs)
        re = relative_error(est, ex)
        print(f"  {name:9s} est {est!r} rel {re!r} rel_fmt {re:.3e} est_fmt {est:.6e}")

xs = stream(1e9)
n = len(xs)
exact_sumsq = sum(Fraction(x) ** 2 for x in xs)
total = 0.0
total_sq = 0.0
for x in xs:
    total += x
    total_sq += x * x
print("offset 1e9 exact sum of squares (float values):", float(exact_sumsq), "as Decimal:", Decimal(exact_sumsq.numerator) / Decimal(exact_sumsq.denominator))
print("computed running total_sq:", repr(total_sq), "difference from exact:", float(Fraction(total_sq) - exact_sumsq), "abs diff", float(abs(Fraction(total_sq) - exact_sumsq)))
print("math.ulp(2e21) =", math.ulp(2e21), " math.ulp(total_sq) =", math.ulp(total_sq))
ex = exact_variance(xs)
print("(n-1)*s^2 exact =", float((n - 1) * ex), " exact Fraction of S_n:", float((n - 1) * ex))
print("naive value repr:", repr(naive(xs)))
print("sys.float_info.mant_dig", sys.float_info.mant_dig)
