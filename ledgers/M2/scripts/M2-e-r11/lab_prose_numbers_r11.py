"""Recompute the bond numbers quoted in project.html Labs 1 and 3 and cards c341/c382 (L23), with the page's own formulas."""
def bond(face, coupon_bps, years, yield_bps):
    y = yield_bps / 10000
    coupon = face * coupon_bps / 10000
    flows = [(t, coupon + (face if t == years else 0.0)) for t in range(1, years + 1)]
    v = 1 / (1 + y)
    P = sum(c * v**t for t, c in flows)
    d1 = -sum(t * c * v ** (t + 1) for t, c in flows)
    d2 = sum(t * (t + 1) * c * v ** (t + 2) for t, c in flows)
    return P, d1, d2, -d1 / P
def price_of(face, coupon_bps, years, y):
    coupon = face * coupon_bps / 10000
    return sum((coupon + (face if t == years else 0.0)) * (1 + y) ** -t for t in range(1, years + 1))
P, d1, d2, dur = bond(1_000_000, 500, 10, 400)
print(f"Lab1 P={P:.4f} rounded={round(P)} dP/dy={d1:.4f} d2P/dy2={d2:.4f} duration={dur:.6f}")
h = 1e-5
cd = (price_of(1_000_000, 500, 10, 0.04 + h) - price_of(1_000_000, 500, 10, 0.04 - h)) / (2 * h)
print(f"Lab1 central dP/dy (step 1e-5, independent evaluation order)={cd:.4f} |diff|={abs(d1 - cd):.3e} relative={abs(d1 - cd) / abs(d1):.3e}")
P3, d13, d23, dur3 = bond(2_500_000, 600, 12, 500)
print(f"Lab3 P={P3:.4f} rounded={round(P3)} dP/dy={d13:.6f}")
c6 = (price_of(2_500_000, 600, 12, 0.05 + 1e-6) - price_of(2_500_000, 600, 12, 0.05 - 1e-6)) / (2e-6)
print(f"Lab3 central dP/dy at step 1e-6, independent evaluation order={c6:.6f} |error|={abs(c6 - d13):.6e} (page prints 7.111207e-04 with its own evaluation order; this is round-off)")
print(f"card c341 unrounded price, face 100000 cents: {price_of(100000, 500, 10, 0.04):.6f}; card c382 rounded: {round(price_of(100000, 500, 10, 0.04))}")
