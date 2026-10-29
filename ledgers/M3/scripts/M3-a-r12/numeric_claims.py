"""Re-derive numeric claims of the M3 slice: L01 R3 floating pivot, L02 misconception 1 identity scope, L02 basis-order matrices, index placement fractions."""
from fractions import Fraction

# L01 R3: columns (1,1) and (1, 1 + 1e-12); float elimination of the 2x2 matrix
t = 1 + 1e-12
pivot_float = t - 1.0          # column 2 minus column 1 after elimination (multiplier 1)
print("float second pivot:", repr(pivot_float), "is below 1e-9:", abs(pivot_float) < 1e-9)
print("exact second pivot: 1e-12 (Fraction):", Fraction(1) + Fraction(1, 10**12) - 1)

# L02 misconception 1: identity map, input basis B and output basis C, coordinates
# B = standard basis, C = ((1,0),(1,1)). Coordinates of e1, e2 in C solve c1*(1,0)+c2*(1,1)=v.
def coords_C(v):
    x, y = v
    c2 = y
    c1 = x - y
    return (c1, c2)
cols = [coords_C((1, 0)), coords_C((0, 1))]
matrix = [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]
print("identity map, B standard, C = ((1,0),(1,1)): matrix", matrix, "equals I:", matrix == [[1, 0], [0, 1]])

# L02 basis order example: projection (x,y)->(x,0)
def proj(v):
    return (v[0], 0)
def matrix_for(basis):
    # basis is ordered pair of vectors; input and output basis both the standard basis
    cols = []
    for b in basis:
        img = proj(b)
        cols.append(tuple(img))
    return [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]
e1, e2 = (1, 0), (0, 1)
# coordinates in the basis (e2, e1): an image w = a*e2 + b*e1 has (a, b) = (w[1], w[0])
def coords_order21(w):
    return (w[1], w[0])
cols21 = [coords_order21(proj(e2)), coords_order21(proj(e1))]
print("basis (e2,e1) matrix (columns in output basis (e1,e2), input basis order (e2,e1)):",
      [[cols21[0][0], cols21[1][0]], [cols21[0][1], cols21[1][1]]])
print("basis (e1,e2) matrix:", matrix_for((e1, e2)))

# index placement fractions
print("80% of 9 =", 0.8 * 9, "; 7/9 =", round(7 / 9 * 100, 1), "; 8/9 =", round(8 / 9 * 100, 1))
print("1+1/2+1/4+1/8 =", 1 + 0.5 + 0.25 + 0.125)
print("100/1.05^2 =", round(100 / 1.05 ** 2, 4), "->", round(100 / 1.05 ** 2, 3))
print("lessons hours:", sum([12, 11, 12, 12, 12, 11, 11, 12, 12]), "; plus project 45 =", sum([12, 11, 12, 12, 12, 11, 11, 12, 12]) + 45)
print("hours split 70/30 of 150:", 105 / 150, 45 / 150)
