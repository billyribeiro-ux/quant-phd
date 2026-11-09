"""High-precision check of 2*exp(sin 1)*cos 1 (the value f_2'(1) for f_2(x) = exp(sin(x^2))), by Taylor series in Decimal."""

from decimal import Decimal, getcontext

getcontext().prec = 60


def exp_d(x: Decimal) -> Decimal:
    term = Decimal(1)
    total = Decimal(1)
    n = 1
    while True:
        term = term * x / n
        if abs(term) < Decimal(10) ** (-58):
            break
        total += term
        n += 1
    return total


def sin_d(x: Decimal) -> Decimal:
    term = x
    total = x
    n = 1
    while True:
        term = -term * x * x / ((2 * n) * (2 * n + 1))
        if abs(term) < Decimal(10) ** (-58):
            break
        total += term
        n += 1
    return total


def cos_d(x: Decimal) -> Decimal:
    term = Decimal(1)
    total = Decimal(1)
    n = 1
    while True:
        term = -term * x * x / ((2 * n - 1) * (2 * n))
        if abs(term) < Decimal(10) ** (-58):
            break
        total += term
        n += 1
    return total


one = Decimal(1)
s1 = sin_d(one)
c1 = cos_d(one)
val = 2 * exp_d(s1) * c1
print("sin 1 =", str(s1)[:20])
print("cos 1 =", str(c1)[:20])
print("exp(sin 1) =", str(exp_d(s1))[:20])
print("2 exp(sin1) cos1 =", str(val)[:30])
print("rounded to 10 decimals:", val.quantize(Decimal("0.0000000001")))
print("truncated to 12 decimals:", str(val)[:15])
print("rounded to 12 decimals:", val.quantize(Decimal("0.000000000001")))
