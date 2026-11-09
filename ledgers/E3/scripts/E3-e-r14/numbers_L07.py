"""Independent recomputation of the L07 weighting-function numbers (verifier round 14, slice e)."""
from decimal import Decimal as D, getcontext
import math

getcontext().prec = 60


def om(p, eta=D("0.5")):
    p = D(p)
    return p ** eta / ((p ** eta + (1 - p) ** eta) ** (1 / eta))


def om_closed(p):
    p = D(p)
    return p.sqrt() / (1 + 2 * (p * (1 - p)).sqrt())


for p in ("0.3", "0.6", "0.5", "0.4", "0.25", "0.01", "0.05", "0.99", "0.95", "0.25", "0.278", "0.279"):
    print("omega", p, "closed", str(om_closed(p))[:16], "general", str(om(p))[:16])
w3 = om_closed("0.3"); w6 = om_closed("0.6"); w4 = om_closed("0.4")
print("ratio w3/w6 to 12 dp", str(w3 / w6)[:16])
print("eight-decimal quotient 0.28579088/0.39125077 =", 0.28579088 / 0.39125077)
print("Gamma(A) alpha 1 =", 150 * w3, " Gamma(B) =", 100 * w6, " diff 40-digit =", str(150 * w3 - 100 * w6)[:16])
print("eight-dp diff =", 42.86863274 - 39.12507700)
print("sum weights A =", w4 + 2 * w3, " 2*w3 =", 2 * w3)
print("w(0.01)*100 + w(0.99)*50 =", 100 * om_closed("0.01") + 50 * om_closed("0.99"))
print("overweight 0.01:", (om_closed("0.01") - D("0.01")) * 100, " underweight 0.99:", (D("0.99") - om_closed("0.99")) * 50)
print("net:", (om_closed("0.01") - D("0.01")) * 100 - (D("0.99") - om_closed("0.99")) * 50)
print("EV", D("0.01") * 100 + D("0.99") * 50)
print("threshold alpha 1/2:", 1 / (1 + 2 ** -0.5), " alpha 1:", 1 / 1.5)
print("E1 ratio check: 1/(2+sqrt3)=", 1 / (2 + D(3).sqrt()), " 2-sqrt3=", 2 - D(3).sqrt())
print("omega(1/2) =", om_closed("0.5"), " 1/(2 sqrt2)=", 1 / (2 * D(2).sqrt()))

# Observation 1.5 on the 1001-point grid (float, as in the lab), plus the sign-change count
grid = [i / 1000 for i in range(1001)]
fl = lambda p: float(p ** 0.5 / ((p ** 0.5 + (1 - p) ** 0.5) ** 2))
inner = grid[1:-1]
above = [fl(p) > p for p in inner]
changes = sum(1 for a, b in zip(above, above[1:]) if a != b)
last = max(p for p in inner if fl(p) > p)
print("grid sign changes", changes, "last above", last)
# eta = 1 check of the closed form (E3 of L07)
gap = max(abs(p - math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))) for p in grid)
argmax = max(grid, key=lambda p: abs(p - math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))))
print("eta=1 closed-form largest gap", gap, "at p", argmax)

# Example 1.4 derivative formula check (verifier round 14): central differences vs omega'(p) closed form
_om = lambda p: math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))
_form = lambda p: (math.sqrt(p * (1 - p)) + 2 * p * p) / (2 * math.sqrt(p) * math.sqrt(p * (1 - p)) * (1 + 2 * math.sqrt(p * (1 - p))) ** 2)
for _p in (0.05, 0.2, 0.3, 0.5, 0.7, 0.95):
    _h = 1e-7
    _num = (_om(_p + _h) - _om(_p - _h)) / (2 * _h)
    print("derivative check p", _p, "numeric", round(_num, 9), "closed form", round(_form(_p), 9), "agree", abs(_num - _form(_p)) < 1e-6)
