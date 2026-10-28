from fractions import Fraction
def cost(h):
    if h == 0: return 0
    return 4000 * (-(-h // 400))  # shifts of 400 h or part thereof
pts = [(0, cost(0)), (1200, cost(1200))]
v = Fraction(pts[1][1] - pts[0][1], pts[1][0] - pts[0][0]); F = pts[0][1] - v * pts[0][0]
errs = [(abs(cost(h) - (F + v * h)), h) for h in range(0, 1201)]
m = max(errs)
print("v", v, "F", F, "max_err", m[0], "at_hours", sorted(h for e, h in errs if e == m[0]))
print("ratio", Fraction(m[0], 4000), float(Fraction(m[0], 4000)))
print("cost over 1..400 values", sorted({cost(h) for h in range(1, 401)}))
print("cost over 0..400 values", sorted({cost(h) for h in range(0, 401)}))
print("line at 1,401,801", [F + v * h for h in (1, 401, 801)], "cost", [cost(h) for h in (1, 401, 801)])
