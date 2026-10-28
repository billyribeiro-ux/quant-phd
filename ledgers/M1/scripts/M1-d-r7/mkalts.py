import re, sys
REF = open("/tmp/verify6-M1-d/course/modules/M/M1/grader/reference.py").read()
def replace_fn(src, name, new):
    pat = re.compile(r"^def " + name + r"\(.*?(?=^def |^class |\Z)", re.S | re.M)
    m = pat.search(src); assert m, name
    return src[:m.start()] + new.rstrip() + "\n\n\n" + src[m.end():]
ALTS = {}
# A: decimal module, ties half-up via ROUND_HALF_UP, high precision
ALTS["alt_decimal_v6"] = {
 "level_payment_cents": '''def level_payment_cents(principal_cents, annual_rate, months):
    from decimal import Decimal, ROUND_HALF_UP, localcontext
    p = _principal(principal_cents)
    r = _annual_rate(annual_rate)
    n = _months(months)
    with localcontext() as ctx:
        ctx.prec = 80
        i = Decimal(repr(r)) / Decimal(12)
        if i == 0:
            amt = Decimal(p) / Decimal(n)
        else:
            amt = Decimal(p) * i / (1 - (1 + i) ** (-n))
        return int(amt.quantize(Decimal(1), rounding=ROUND_HALF_UP))
''',
 "amortization_schedule": '''def amortization_schedule(principal_cents, annual_rate, months):
    from decimal import Decimal, ROUND_HALF_UP, localcontext
    p = _principal(principal_cents)
    r = _annual_rate(annual_rate)
    n = _months(months)
    pay = level_payment_cents(p, r, n)
    rows = []
    opening = p
    with localcontext() as ctx:
        ctx.prec = 80
        i = Decimal(repr(r)) / Decimal(12)
        for k in range(1, n + 1):
            interest = int((Decimal(opening) * i).quantize(Decimal(1), rounding=ROUND_HALF_UP))
            paid = pay if k < n else opening + interest
            closing = opening - (paid - interest)
            rows.append(ScheduleRow(k, opening, interest, paid - interest, paid, closing))
            opening = closing
    return tuple(rows)
''',
}
# B: exact Fraction summation for the level payment (sum of discount factors), closed form for schedule
ALTS["alt_fraction_sum_v6"] = {
 "level_payment_cents": '''def level_payment_cents(principal_cents, annual_rate, months):
    from fractions import Fraction as F
    import math as m
    p = _principal(principal_cents)
    r = _annual_rate(annual_rate)
    n = _months(months)
    i = F(repr(r)) / 12
    if i == 0:
        q = F(p, n)
    else:
        a = sum((1 / (1 + i)) ** k for k in range(1, n + 1))
        q = F(p) / a
    return m.floor(q + F(1, 2))
''',
}
# C: float algorithms with expm1/log1p, and a numerical cutoff for a zero rate (1e-12 a month)
ALTS["alt_expm1_cutoff_v6"] = {
 "annuity_factor": '''def annuity_factor(rate, periods):
    r = _real("rate", rate)
    n = _periods("periods", periods)
    if r <= -1:
        raise ValueError("rate must be greater than -1 per period")
    if n == 0:
        return 0.0
    if abs(r) < 1e-12:
        return float(n)
    import math as m
    return -m.expm1(-n * m.log1p(r)) / r
''',
 "level_payment_cents": '''def level_payment_cents(principal_cents, annual_rate, months):
    principal = _principal(principal_cents)
    i = _exact_rate(_annual_rate(annual_rate)) / 12
    n = _months(months)
    if abs(i) < Fraction(1, 10**12):
        return _nearest_cent(Fraction(principal, n))
    return _nearest_cent(principal * i / (1 - (1 + i) ** -n))
''',
}
# D: schedule via Fraction, with exact arithmetic but a different loop (closing computed from closed-form balance)
ALTS["alt_balance_closed_form_v6"] = {
 "amortization_schedule": '''def amortization_schedule(principal_cents, annual_rate, months):
    principal = _principal(principal_cents)
    rate = _annual_rate(annual_rate)
    n = _months(months)
    i = _exact_rate(rate) / 12
    payment = level_payment_cents(principal, rate, n)
    out = []
    opening = principal
    for k in range(1, n + 1):
        interest = _nearest_cent(Fraction(opening) * i)
        if k == n:
            paid = opening + interest
        else:
            paid = payment
        closing = opening + interest - paid
        out.append(ScheduleRow(period=k, opening_cents=opening, interest_cents=interest,
                               principal_cents=paid - interest, payment_cents=paid, closing_cents=closing))
        opening = closing
    return tuple(out)
''',
}
for name, fns in ALTS.items():
    s = REF
    for f, body in fns.items():
        s = replace_fn(s, f, body)
    open(f"/tmp/m1-v6/d/alts/{name}.py", "w").write(s)
    print("wrote", name)
