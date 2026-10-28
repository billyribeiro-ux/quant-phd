import re
exec(open("/tmp/m1-v6/d/mkalts.py").read().split("ALTS = {}")[0])
ALTS = {
 "alt_float_epsilon_v6": {"level_payment_cents": '''def level_payment_cents(principal_cents, annual_rate, months):
    import math
    p = _principal(principal_cents)
    r = _annual_rate(annual_rate)
    n = _months(months)
    i = r / 12
    if i == 0:
        return math.floor(p / n + 0.5 + 1e-9)
    return math.floor(p * i / (1 - (1 + i) ** -n) + 0.5 + 1e-9)
'''},
 "alt_fraction_binary_v6": {"level_payment_cents": '''def level_payment_cents(principal_cents, annual_rate, months):
    import math
    from fractions import Fraction as F
    p = _principal(principal_cents)
    r = _annual_rate(annual_rate)
    n = _months(months)
    i = F(r) / 12
    if i == 0:
        return math.floor(F(p, n) + F(1, 2))
    return math.floor(p * i / (1 - (1 + i) ** -n) + F(1, 2))
'''},
}
for name, fns in ALTS.items():
    s = REF
    for f, body in fns.items():
        s = replace_fn(s, f, body)
    open(f"/tmp/m1-v6/d/alts/{name}.py", "w").write(s)
    print("wrote", name)
