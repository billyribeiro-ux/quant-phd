# Zero map on R^2 with input basis (e1, e2) and reordered input basis (e2, e1), output basis (e1, e2).
from fractions import Fraction
def matrix_of(L, basis, out_basis):
    # columns: coordinates of L(b_j) in out_basis (standard coordinates here)
    cols = [L(b) for b in basis]
    return [[cols[j][i] for j in range(len(basis))] for i in range(2)]
zero = lambda v: (Fraction(0), Fraction(0))
e1, e2 = (Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))
M = matrix_of(zero, [e1, e2], None)
M2 = matrix_of(zero, [e2, e1], None)
print("zero map, basis (e1,e2):", M)
print("zero map, reordered (e2,e1):", M2, "| basis vector moved:", [e2, e1] != [e1, e2], "| matrix unchanged:", M == M2)
# projection onto first coordinate, reordered input basis: matrix changes, as the sentence says
proj = lambda v: (v[0], Fraction(0))
print("projection, (e1,e2):", matrix_of(proj, [e1, e2], None), " reordered (e2,e1):", matrix_of(proj, [e2, e1], None))
