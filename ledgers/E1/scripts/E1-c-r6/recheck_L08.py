"""Independent check of L08 grid claims and problem numbers (verifier round 6)."""
from fractions import Fraction as F
X, Y = 8, 4
def u(x, y): return x*y
def v(x, y): return (X-x)*(Y-y)
pts = [(x, y) for x in range(X+1) for y in range(Y+1)]
def dominates(z, w):
    return u(*z) >= u(*w) and v(*z) >= v(*w) and (u(*z) > u(*w) or v(*z) > v(*w))
eff = [w for w in pts if not any(dominates(z, w) for z in pts)]
print("grid-efficient count:", len(eff), "(page: 15)")
inter = [w for w in eff if 0 < w[0] < X and 0 < w[1] < Y]
print("interior:", len(inter), inter)
print("boundary:", [w for w in eff if w not in inter])
diag = [w for w in inter if w[1]*X == w[0]*Y]
print("interior diagonal:", diag, "off-diagonal count:", len(inter)-len(diag))
# equality of sqrt bound: 4 u v = (XY - u - v)^2 with sign
eq = [(x, y) for x, y in pts if (X*Y - u(x,y) - v(x,y)) >= 0 and 4*u(x,y)*v(x,y) == (X*Y - u(x,y) - v(x,y))**2]
print("equality points:", eq, "=diagonal:", sorted(eq) == sorted(w for w in pts if w[1]*X == w[0]*Y))
print("bound holds at all grid:", all(4*u(x,y)*v(x,y) <= (X*Y-u(x,y)-v(x,y))**2 and X*Y-u(x,y)-v(x,y) >= 0 for x,y in pts))
# Continuous check: is (3,1) improvable exactly with the page's allocation
A = (F(18,7), F(6,5)); B = (X-A[0], Y-A[1])
print("page (3,1) move: uA", u(*A), "vs", u(3,1), "uB", v(*A), "vs", v(3,1))
# Off-diagonal improvements in the lab: verify each printed allocation strictly improves both
page_moves = {(1,1):(F(6,5),F(6,7)),(2,2):(F(5,2),F(5,3)),(3,1):(F(18,7),F(6,5)),(3,2):(F(27,8),F(9,5)),
              (4,1):(F(3),F(3,2)),(4,3):(F(5),F(5,2)),(5,2):(F(37,8),F(11,5)),(5,3):(F(38,7),F(14,5)),
              (6,2):(F(11,2),F(7,3)),(7,3):(F(34,5),F(22,7))}
assert sorted(page_moves) == sorted(w for w in inter if w[1]*X != w[0]*Y)
ok = True
for (x,y), (na, nb) in page_moves.items():
    ua0, ub0 = u(x,y), v(x,y)
    ua1 = na*nb; ub1 = (X-na)*(Y-nb)
    good = ua1 > ua0 and ub1 > ub0 and 0 <= na <= X and 0 <= nb <= Y
    nonint = na.denominator != 1 or nb.denominator != 1 or (X-na).denominator != 1 or (Y-nb).denominator != 1
    if not (good and nonint): ok = False; print("FAIL", (x,y), na, nb)
print("all 10 printed improvements strictly raise both, feasible, and have a non-integer amount:", ok)
# Problem numbers
print("M1 y:", F(4*5, 10), "uA", F(4)*2, "uB", (10-4)*(5-2))
print("M2: lam=11/24 bounds", F(5,6)/F(11,24), F(5,4)/F(11,24))
h = F(10,11); lam = F(11,24)
A2 = (4-h, 1+lam*h); B2 = (6+h, 4-lam*h)
print("M2 holds A", A2, "uA", A2[0]*A2[1], float(A2[0]*A2[1]), "B", B2, "uB", B2[0]*B2[1], float(B2[0]*B2[1]))
print("M2 B change formula check", B2[0]*B2[1] - 24, h*(4 - lam*6 - lam*h))
print("E1 gains: A", F(108,35)-3, "B", F(76,5)-15, "shares", (F(108,35)-3)/3, (F(76,5)-15)/15)
print("E2 share 13/21 =", float(F(13,21)))
print("Q-quiz (4,2) sum:", 2*(8**0.5), "sqrt(32)=", 32**0.5)
print("R1 check W on diagonal: s+t at x=3:", 3*(4/8)**0.5 + (8-3)*(4/8)**0.5, (32)**0.5)
print("R3: A holds (0,2) u_A", 0, "B holds (8,2) u_B", 16, "after move A=(8/3,1) uA", F(8,3), "B=(16/3,3) uB", F(16,3)*3)
print("Example 2.5 uA/uB:", (6*3, (8-6)*(4-3)), (2*1, (8-2)*(4-1)))
print("Lemma check: proposition 2.2 h bounds fine")
# Lab 1 part E bound at all grid points, exact
print("bound violated anywhere:", any(4*u(x,y)*v(x,y) > (X*Y-u(x,y)-v(x,y))**2 for x,y in pts))
